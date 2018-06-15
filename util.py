import psycopg2
import psycopg2.extras

import usaddress

from collections import OrderedDict as OD
import json
import csv
from django.forms.models import model_to_dict
from django.contrib.gis.db.models.functions import Scale


from wprdc_tools import settings
from .models import Parcel, AdminRegion, AddressPoint, RegionType

from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

AVAILABLE_METHODS = ('download',)
AVAILABLE_FORMATS = ('json', 'geojson',)

QRY_TEMPLATE = """
SELECT a.gid,
    a.pin,
    a.geom
   FROM parcel_boundaries a
  WHERE st_intersects(( SELECT {region_table}.geom
           FROM {region_table}
          WHERE (({region_table}.hood)::TEXT = '{region_name}'::TEXT)), a.geom)
"""

FC_QRY_TEMPLATE = """
SELECT row_to_json(fc)
 FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features
 FROM (SELECT 'Feature' As type
    , ST_AsGeoJSON(lg.geom)::json As geometry
    , row_to_json((SELECT l FROM (SELECT pin) As l
      )) As properties
   FROM ({inner_query}) As lg   ) As f )  As fc;
"""


def parcels_in_region(region_type, region_name):
    conn = psycopg2.connect("dbname=geo")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    inner_qry = QRY_TEMPLATE.format(
        region_table=region_type, region_name=region_name)
    qry = FC_QRY_TEMPLATE.format(inner_query=inner_qry)
    cur.execute(qry)
    stuff = cur.fetchall()[0]

    conn.close()
    with open('stuff.json', 'w') as f:
        json.dump(stuff, f)

    return stuff[0]


def parse_options(get_params, available_formats=AVAILABLE_FORMATS, available_methods=AVAILABLE_METHODS):
    if 'format' in get_params:
        f = get_params['format']

        if f not in AVAILABLE_FORMATS:
            f = 'json'
    else:
        f = 'json'

    # Set response method (text, or download)
    if 'method' in get_params:
        m = get_params['type']
        if m not in AVAILABLE_METHODS:
            m = 'text'
    else:
        m = 'text'

    return f, m


def parse_coord_string(coord_string):
    x, y = coord_string.split(',')
    return float(x), float(y)


def parse_address_string(addr_str):
    """
    Parses address string into constituent parts.
    Currently uses usaddress (https://github.com/datamade/usaddress)

    :param addr_str: address string to be parsed
    :return: dict of address parts
    """
    address_parts, address_type = usaddress.tag(addr_str)

    # Get just first letter of Directional e.g. S from South Craig
    if 'StreetNamePreDirectional' in address_parts:
        directional = address_parts['StreetNamePreDirectional'][0]
    else:
        directional = ''

    return ({
        'number': address_parts.get('AddressNumber', '').upper(),
        'directional': directional,
        'street_name': address_parts.get('StreetName', '').upper(),
        'street_type': fix_street_type(address_parts.get('StreetNamePostType', '').upper()),
        'city': address_parts.get('PlaceName', '').upper(),
        'state': address_parts.get('StateName', '').upper(),
        'zip_code': address_parts.get('ZipCode', '').upper(),
    })


def geocode_from_address_parts(addr_parts):
    """
    :param addr_parts: dict of address par
    :return: Point representing location fo address
    """

    # First try to get address point
    point = geocode_address_point(addr_parts)

    # If that fails, check parcel data
    if not point:
        point = geocode_parcel_centroid(addr_parts)

    return point


def geocode_from_address_string(addr_str):
    return geocode_from_address_parts(parse_address_string(addr_str))


def geocode_address_point(addr_parts):
    # first, try with zip
    addr = AddressPoint.objects.filter(
        address_number=addr_parts['number'],
        street_prefix=addr_parts['directional'],
        street_name__startswith=addr_parts['street_name'],
        street_type=addr_parts['street_type'],
        zip_code=addr_parts['zip_code']
    )

    if not addr:
        addr = AddressPoint.objects.filter(
            address_number=addr_parts['number'],
            street_prefix=addr_parts['directional'],
            street_name__startswith=addr_parts['street_name'],
            street_type=addr_parts['street_type'],
            city__startswith=addr_parts['city']
        )

    if addr:
        return addr[0].geom
    else:
        return None


def geocode_parcel_centroid(addr_parts):
    street = addr_parts['street_name']
    if addr_parts['directional']:
        street = addr_parts['directional'] + ' ' + street

    parcels = Parcel.objects.filter(
        addr_number=addr_parts['number'],
        addr_street__startswith=street,
        addr_zip=zip
    )
    if not parcels:
        parcels = Parcel.objects.filter(
            addr_number=addr_parts['number'],
            addr_street__startswith=street,
            addr_zip=zip
        )

    if parcels:
        return parcels[0].geom
    else:
        return None


def geocode_file(input_file, address_field):
    fields = []
    output_rows = []
    # open user's file
    with open(settings.BASE_DIR + input_file) as f:
        dr = csv.DictReader(f)
        fields = dr.fieldnames

        # for each record in file, geocode address
        for row in dr:
            addr = row[address_field]
            geo_data = forward_geocode(addr)

            if len(geo_data):
                if 'coordinates' in geo_data['geom']:
                    coords = geo_data['geom']['coordinates']
                else:
                    coords = []

                regions = {k: v['name']
                           for k, v in geo_data['regions'].items()}

                new_row = {**regions,
                           **{'parcel_id': geo_data['parcel_id'], 'coordinates': coords}}

                # make new row with user's data and geo_data
                output_rows.append({**row, **new_row})

                # keep track of new header
                for k in new_row.keys():
                    if k not in fields:
                        fields.append(k)
            else:
                output_rows.append(dict(row))

    return output_rows, fields


def get_parcel_regions(parcel):
    pin = parcel.pin
    regions = AdminRegion.objects.filter(geom__contains=parcel.geom.centroid)
    return {region.type.id: region.name for region in regions}


def fix_street_type(street_type):
    mapping = {'CIR': 'CIR', 'BG': 'BG', 'LKS': 'LKS', 'HILLS': 'HLS', 'PLNS': 'PLNS', 'SHLS': 'SHLS', 'WLS': 'WLS',
               'PARK': 'PARK', 'CPE': 'CPE', 'BRG': 'BRG', 'EXT': 'EXT', 'STREET': 'ST', 'CRESCENT': 'CRES', 'BR': 'BR',
               'FALL': 'FALL', 'BLVD': 'BLVD', 'COURT': 'CT', 'FORKS': 'FRKS', 'BEACH': 'BCH', 'GARDENS': 'GDNS',
               'VL': 'VL', 'HBR': 'HBR', 'PIKE': 'PIKE', 'GLN': 'GLN', 'HOLLOW': 'HOLW', 'BOTTOM': 'BTM', 'RIV': 'RIV',
               'LCKS': 'LCKS', 'FGR': 'FGR', 'RD': 'RD', 'PRT': 'PRT', 'SUMMIT': 'SMT', 'TERRACE': 'TER',
               'VALLEY': 'VLY', 'ROAD': 'RD', 'SPG': 'SPG', 'ORCH': 'ORCH', 'CRSE': 'CRSE', 'GROVE': 'GRV',
               'CLFS': 'CLFS', 'COVE': 'CV', 'BYP': 'BYP', 'PASS': 'PASS', 'ISLANDS': 'ISS', 'RIVER': 'RIV',
               'SPUR': 'SPUR', 'BND': 'BND', 'GTWY': 'GTWY', 'VIA': 'VIA', 'XING': 'XING', 'HARBOR': 'HBR',
               'LAKE': 'LK', 'LANDING': 'LNDG', 'ARC': 'ARC', 'TRAIL': 'TRL', 'TUNL': 'TUNL', 'RADIAL': 'RADL',
               'CIRCLE': 'CIR', 'EXPRESSWAY': 'EXPY', 'ISLE': 'ISLE', 'LOOP': 'LOOP', 'VIEW': 'VW', 'JCT': 'JCT',
               'BURG': 'BG', 'LIGHT': 'LGT', 'FLS': 'FLS', 'FLT': 'FLT', 'LNDG': 'LNDG', 'FREEWAY': 'FWY',
               'FORGE': 'FGR', 'SHORE': 'SHR', 'BOULEVARD': 'BLVD', 'HL': 'HL', 'CRK': 'CRK', 'ST': 'ST',
               'AVENUE': 'AVE', 'MEADOWS': 'MDWS', 'DIVIDE': 'DV', 'PR': 'PR', 'MOUNTAIN': 'MTN', 'LDG': 'LDG',
               'CENTER': 'CTR', 'BCH': 'BCH', 'VIS': 'VIS', 'FIELDS': 'FLDS', 'MNR': 'MNR', 'PKY': 'PKY',
               'WELLS': 'WLS', 'FALLS': 'FLS', 'VLY': 'VLY', 'PLAINS': 'PLNS', 'MALL': 'MALL', 'HILL': 'HL',
               'BYPASS': 'BYP', 'VILLAGE': 'VLG', 'SPRINGS': 'SPGS', 'PL': 'PL', 'ROW': 'ROW', 'GRV': 'GRV',
               'LOAF': 'LF', 'SQUARE': 'SQ', 'INLET': 'INLT', 'FOR': 'FOR', 'UNION': 'UN', 'BROOK': 'BRK',
               'PLAZA': 'PLZ', 'EXPY': 'EXPY', 'BAYOU': 'YU', 'PLACE': 'PL', 'PLN': 'PLN', 'LODGE': 'LDG',
               'FERRY': 'FRY', 'TRCE': 'TRCE', 'FORD': 'FOR', 'SHL': 'SHL', 'TRAILER': 'TRLR', 'GLEN': 'GLN',
               'DR': 'DR', 'NECK': 'NCK', 'TRACE': 'TRCE', 'COURSE': 'CRSE', 'TRACK': 'TRAK', 'ML': 'ML',
               'VIADUCT': 'VIA', 'TPKE': 'TPKE', 'MT': 'MT', 'UN': 'UN', 'HTS': 'HTS', 'RPDS': 'RPDS', 'SHOAL': 'SHL',
               'CROSSING': 'XING', 'SHRS': 'SHRS', 'STRA': 'STRA', 'FLD': 'FLD', 'HAVEN': 'HVN', 'COR': 'COR',
               'JUNCTION': 'JCT', 'STREAM': 'STRM', 'CTS': 'CTS', 'ISS': 'ISS', 'SPRING': 'SPG', 'SMT': 'SMT',
               'FLDS': 'FLDS', 'LAKES': 'LKS', 'STATION': 'STA', 'BEND': 'BND', 'COURTS': 'CTS', 'CAPE': 'CPE',
               'OVAL': 'OVAL', 'CORNER': 'COR', 'LANE': 'LN', 'BLF': 'BLF', 'MANOR': 'MNR', 'POINT': 'PT',
               'TUNNEL': 'TUNL', 'FWY': 'FWY', 'MISSION': 'MSN', 'CAUSEWAY': 'CSWY', 'FRKS': 'FRKS', 'HIGHWAY': 'HWY',
               'TRL': 'TRL', 'HWY': 'HWY', 'TER': 'TER', 'VISTA': 'VIS', 'RIDGE': 'RDG', 'ORCHARD': 'ORCH',
               'PLAIN': 'PLN', 'MOUNT': 'MT', 'MILLS': 'MLS', 'CLB': 'CLB', 'FRST': 'FRST', 'FIELD': 'FLD',
               'RDG': 'RDG', 'KNLS': 'KNLS', 'WAY': 'WAY', 'CORS': 'CORS', 'SHR': 'SHR', 'FRY': 'FRY', 'CP': 'CP',
               'CV': 'CV', 'CT': 'CT', 'VILLE': 'VL', 'RADL': 'RADL', 'RUN': 'RUN', 'CREEK': 'CRK', 'VW': 'VW',
               'HVN': 'HVN', 'ISLAND': 'IS', 'SQ': 'SQ', 'PLZ': 'PLZ', 'TRAK': 'TRAK', 'VLG': 'VLG', 'LOCKS': 'LCKS',
               'BRK': 'BRK', 'KEY': 'CY', 'ALY': 'ALY', 'TURNPIKE': 'TPKE', 'ESTATES': 'EST', 'BRANCH': 'BR',
               'DALE': 'DL', 'BRIDGE': 'BRG', 'DL': 'DL', 'CRES': 'CRES', 'TRLR': 'TRLR', 'CSWY': 'CSWY',
               'EXTENSION': 'EXT', 'MDWS': 'MDWS', 'HLS': 'HLS', 'GN': 'GN', 'DRIVE': 'DR', 'WALK': 'WALK',
               'MSN': 'MSN', 'GREEN': 'GN', 'STA': 'STA', 'DV': 'DV', 'PATH': 'PATH', 'PARKWAY': 'PKY', 'YU': 'YU',
               'STRAVENUES': 'STRA', 'KNOLLS': 'KNLS', 'ARCADE': 'ARC', 'LN': 'LN', 'DAM': 'DM', 'CAMP': 'CP',
               'LK': 'LK', 'ALLEY': 'ALY', 'PORT': 'PRT', 'PRAIRIE': 'PR', 'FOREST': 'FRST', 'BLUFF': 'BLF',
               'CORNERS': 'CORS', 'PINES': 'PNES', 'CLIFFS': 'CLFS', 'DM': 'DM', 'CYN': 'CYN', 'FORK': 'FORK',
               'LF': 'LF', 'CTR': 'CTR', 'EST': 'EST', 'STRM': 'STRM', 'RAPIDS': 'RPDS', 'HOLW': 'HOLW', 'INLT': 'INLT',
               'IS': 'IS', 'RANCH': 'RNCH', 'SHOALS': 'SHLS', 'RNCH': 'RNCH', 'REST': 'RST', 'HEIGHTS': 'HTS',
               'SHORES': 'SHRS', 'BTM': 'BTM', 'CANYON': 'CYN', 'MTN': 'MTN', 'FT': 'FT', 'AVE': 'AVE', 'FLATS': 'FLT',
               'MILL': 'ML', 'CLUB': 'CLB', 'FORT': 'FT', 'GDNS': 'GDNS', 'MLS': 'MLS', 'SPGS': 'SPGS', 'PT': 'PT',
               'ANNEX': 'ANX', 'ANX': 'ANX', 'PNES': 'PNES', 'CY': 'CY', 'NCK': 'NCK', 'RST': 'RST', 'GATEWAY': 'GTWY',
               'LGT': 'LGT'}

    try:
        result = mapping[street_type]
    except:
        result = ''
    return result


def forward_geocode(address):
    """
    Looks up geo data pertaining to `address`

    :param address:
    :return:
    """
    result = OD([('geom', {}), ('parcel_id', ''),
                 ('regions', {}), ('status', 'ERROR')])
    try:
        # get point
        point = geocode_from_address_string(address)
        result['geom'] = {'type': 'Point', 'coordinates': list(point.coords)}
        result['status'] = 'WARNING: Only found point of address'

        # get regions
        regions = AdminRegion.objects.filter(geom__contains=point)
        result['regions'] = {region.type.id: {
            'id': region.name, 'name': region.title} for region in regions}
        result['status'] = 'WARNING: Only found point of address and regions'

        # get parcel
        parcels = Parcel.objects.filter(geom__contains=point)
        if not parcels:
            close_parcels = Parcel.objects.filter(
                geom__dwithin=(point, 0.0002))
            ordered_parcels = sorted(close_parcels.annotate(
                distance=Distance('geom', point)), key=lambda obj_: obj_.distance)
            parcel = ordered_parcels[0]
            result['status'] = 'WARNING: using closed parcel to address point.'
        else:
            parcel = parcels[0]
            result['status'] = 'OK'
        result['parcel_id'] = parcel.pin

    finally:
        return result


def spatial_query(region_type, region_name, method):
    BUFFER_BASE = 0.000180063
    if method in ['intersects', 'contains']:
        buffer = BUFFER_BASE * -1
    else:
        buffer = BUFFER_BASE

    data = {}
    region = AdminRegion.objects.filter(type=region_type, name=region_name)[0]
    filter_kwargs = {"geom__{}".format(
        method): region.geom.buffer(buffer)}

    other_regions = AdminRegion.objects.filter(**filter_kwargs)

    for r in RegionType.objects.all():
        data[r.id] = [model_to_dict(n, exclude=['geom', 'type'])
                      for n in other_regions.filter(type=r.id)]
    return data
