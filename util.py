import psycopg2
import psycopg2.extras

import usaddress

from collections import OrderedDict as OD
import json
import csv
import re
from django.forms.models import model_to_dict
from django.contrib.gis.db.models.functions import Scale


from wprdc_tools import settings
from .models import Parcel, AdminRegion, AddressPoint, RegionType

from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from pprint import pprint

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

cardinal_direction = {'N': 'NORTH', 'E': 'EAST',
                      'S': 'SOUTH', 'W': 'WEST'}

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

    street_name = address_parts.get('StreetName', '').upper()
    street_type = fix_street_type(address_parts.get('StreetNamePostType', '').upper())
    city = address_parts.get('PlaceName', '').upper()
    zip_code = address_parts.get('ZipCode', '').upper()[:5]
    if 'StreetNamePreType' in address_parts: # Example: Avenue F parses this way.
        street_name = address_parts.get('StreetNamePreType', '').upper() + ' ' + street_name

    if street_name == 'PROSPECT' and street_type in ['TER', 'TERR', 'TERRACE'] and zip_code == '15112':
        street_type = 'DR' # Correct mismatch between database and common address represenation.

    if city == 'PGH':
        city = 'PITTSBURGH'

    if directional.upper() == 'E' and street_name in ['PITTSBURGH MCKEESPORT', 'PGH MCKEESPORT', 'PGH MCK', 'PITTSBURGH MCK']:
        directional = ''
        street_name = 'EAST PITTSBURGH MCKEESPORT'

    if directional.upper() == 'E' and street_name == 'LIBERTY':
        directional = ''
        street_name = 'EAST LIBERTY'

    if directional.upper() == 'E' and street_name == 'END':
        directional = ''
        street_name = 'EAST END'

    if directional.upper() == 'E' and street_name == 'HILLS':
        directional = ''
        street_name = 'EAST HILLS'

    if directional.upper() == 'N' and street_name == 'FLORENCE' and zip_code == '15237':
        directional = ''
        street_name = 'NORTH FLORENCE'

    if directional.upper() == 'W' and street_name == 'RUN' and zip_code in ['15207', '15120']:
        directional = ''
        street_name = 'WEST RUN'

    if directional.upper() == 'W' and street_name == 'VIEW' and zip_code in ['15237', '15229']:
        directional = ''
        street_name = 'WEST VIEW'

    if directional.upper() == 'W' and street_name == 'LIBERTY' and zip_code in ['15216', '15226']:
        directional = ''
        street_name = 'WEST LIBERTY'

    if directional.upper() == 'W' and street_name == 'WOOD' and zip_code in ['15122', '15209', '15235', '15044', '15211']:
        directional = ''
        street_name = 'WESTWOOD'

    if street_name in ['ICE PLANT HILL', 'ICEPLANT HILL', 'ICEPLANT']:
        street_name = 'ICE PLANT' # This addresses an issue in the AddressPoint database
        # or at least a lack of nuance.

# Streets with type VLG that may be getting 'VILLAGE' lumped in with their street name:
# {'HARRISON VLG, MCKEESPORT 15132', 'SOUTH HILLS VLG, BETHEL PARK 15241', 'SOUTH HILLS VLG, UPPER ST CLAIR 15241', 'HAWKINS VLG, RANKIN 15104', 'CRAWFORD VLG, MCKEESPORT 15132', 'LAUREL VLG, BEN AVON 15202'}
    if street_name == ['CRAWFORD VILLAGE', 'CRAWFORD VILL', 'CRAWFORD VLG'] and street_type == '' and zip_code in ['15132']:
        street_name = 'CRAWFORD'
        street_type = 'VLG'
    if street_name in ['HARRISON VILLAGE', 'HARRISON VILL', 'HARRISON VLG'] and street_type == '' and zip_code in ['15132']:
        street_name = 'HARRISON'
        street_type = 'VLG'
    if street_name == ['HAWKINS VILLAGE', 'HAWKINS VILL', 'HAWKINS VLG'] and street_type == '' and zip_code in ['15104']:
        street_name = 'HAWKINS'
        street_type = 'VLG'
    if street_name == ['LAUREL VILLAGE', 'LAUREL VILL', 'LAUREL VLG'] and street_type == '' and zip_code in ['15202']:
        street_name = 'LAUREL'
        street_type = 'VLG'
    if street_name == ['SOUTH HILLS VILLAGE', 'SOUTH HILLS VILL', 'SOUTH HILLS VLG'] and street_type == '' and zip_code in ['15241']:
        street_name = 'SOUTH HILLS'
        street_type = 'VLG'

    if street_name in ['ALPAN VILLAGE', 'ALPAN VILL', 'ALPAN VLG', 'ALPINE VILL', 'ALPINE VLG'] and zip_code in ['15146']:
        street_name = 'ALPINE VILLAGE' # The full name is ALPINE VILLAGE DRIVE.

    if street_name in ['BROWNVILLE', 'BROWSVILLE', 'BROWNSVILLLE'] and zip_code in ['15210', '15236', '15129', '15227', '15332']:
        street_name = 'BROWNSVILLE'

    if street_name in ['CATHERINE', 'CATHRINE', 'KATHERINE', 'KATHRINE', 'KATHARINE'] and zip_code in ['15110']:
        street_name = 'CATHARINE'
    if street_name in ['CHARLEMANE', 'CHARLEMANGE'] and zip_code in ['15237']:
        street_name = 'CHARLEMAGNE'
    if street_name in ['CHARLEMA'] and zip_code in ['15214']:
        street_name = 'CHARLEMMA'

    if street_name in ['GLENMAWR'] and zip_code in ['15204', '15220']:
        street_name = 'GLEN MAWR'
    if street_name == 'GLEN MAWR' and zip_code in ['15204', '15220']:
        street_type = 'AVE'
    if street_name in ['GLENSHANNON'] and zip_code in ['15234']:
        street_name = 'GLEN SHANNON'
    if street_name in ['GREENVALLEY'] and zip_code in ['15116', '15237', '15235', '15220']:
        street_name = 'GREEN VALLEY'

    if street_name == 'HAWKING' and zip_code in ['15122', '15104', '15214']:
        street_name = 'HAWKINS'
    if street_name == 'HOLLYLYNNE' and zip_code in ['15236', '15102']:
        street_name = 'HOLLY LYNNE'
    if street_name in ['JAMES HENERY JUNIOR', 'JAMES HENRY JUNIOR', 'JAMES HENERY JR']:
        street_name = 'JAMES HENRY JR'
    if street_name in ['MARGERET', 'MARGERT', 'MARGRET'] and zip_code in ['15210', '15104', '15126', '15227', '15238', '15046', '15136', '15089', '15106', '15120', '15235', '15209', '15017']:
        street_name = 'MARGARET'
    if street_name in ['MILLVILLE', 'MILLVILL'] and zip_code in ['15213', '15238', '15224']:
        street_name = 'MILLVALE'


    if street_name == 'OAKHILL' and street_type in ['DR', 'DRIVE'] and zip_code in ['15213']:
        street_name = 'OAK HILL'
    if street_name == 'OAKLYNN' and zip_code in ['15220']:
        street_name = 'OAK LYNN'
    if street_name == 'PARKHILL' and zip_code in ['15221']:
        street_name = 'PARK HILL'

    if street_name in ['RUSSELWOOD'] and zip_code in ['15136']:
        street_name = 'RUSSELLWOOD'

    # Handle misspellings of "SAINT" ==> "ST" street names first.
    if street_name in ['ST CLAIRE', "SAINT CLAIRE"]:
        street_name = 'SAINT CLAIR'
    if street_name in ['ST CROI', 'ST CROY', 'SAINT CROY']:
        street_name = 'SAINT CROIX'
    if street_name in ['ST JOHNS', "ST JOHN'S"]:
        street_name = 'SAINT JOHNS'
    if street_name in ['ST AGNES', 'ST ANDREW', 'ST ANDREWS', 'ST ANN', 'ST ANNE', 'ST CHARLES', 'ST CLAIR', 'ST CROIX', 'ST DAVID', 'ST GEORGE', 'ST GERMAINE', 'ST IVES', 'ST JAMES', 'ST JOHN', 'ST JOHNS', 'ST JOSEPH', 'ST LAWRENCE', 'ST LEO', 'ST LUCAS', 'ST MARIE', 'ST MARKS', 'ST MARTIN', 'ST MARTINS', 'ST MARYS', 'ST MELLION', 'ST MICHAEL', 'ST MORITZ', 'ST NORBERT', 'ST PATRICK', 'ST PAUL', 'ST PETER', 'ST REGIS', 'ST ROSE', 'ST SIMON', 'ST SUSANNA', 'ST THERESE', 'ST THOMAS', 'ST VINCENT', 'ST WILLIAM']:
        street_name = re.sub('^ST ', 'SAINT ', street_name)

    if street_name in ['STUBENVILLE'] and zip_code in ['15205', '15071', '15126', '15275', '15136', '15057']:
        street_name = 'STEUBENVILLE'

    if street_name in ['SWISSVILLE'] and zip_code in ['15221']:
        street_name = 'SWISSVALE'

    if street_name in ['SUMMERVILLE'] and zip_code in ['15201', '15243', '15241']:
        street_name = 'SOMERVILLE'

    if street_name in ['VELONA'] and zip_code in ['15147', '15104', '15235', '15206']:
        street_name = 'VERONA'
    if street_name in ['WM PENN'] and zip_code in ['15219', '15221', '15063', '15145', '15143', '15235', '15146']:
        street_name = 'WILLIAM PENN'

    if street_name == 'CAMBRIDGE' and street_type in ['SQ', 'SQUARE'] and zip_code in ['15146']:
        street_name = 'CAMBRIDGE SQUARE'
        street_type = 'DR'

    if street_name == 'HILL SIDE' and zip_code in ['15219']:
        street_name = 'HILLSIDE'

    if street_name == 'MT PLEASANT':
        street_name = 'MOUNT PLEASANT'

    if street_name == 'FIRST':
        street_name = '1ST'

    if street_name == 'SECOND':
        street_name = '2ND'

    if street_name == 'THIRD':
        street_name = '3RD'

    if street_name == 'FOURTH':
        street_name = '4TH'

    if street_name == 'FIFTH':
        street_name = '5TH'

    if street_name == 'SIXTH':
        street_name = '6TH'

    if street_name == 'SEVENTH':
        street_name = '7TH'

    if street_name == 'EIGHTH':
        street_name = '8TH'

    if street_name == 'NINTH':
        street_name = '9TH'

    if street_name == 'TENTH':
        street_name = '10TH'

    if street_name == 'ELEVENTH':
        street_name = '11TH'

    if street_name == 'TWELFTH':
        street_name = '12TH'

    if street_name == 'THIRTEENTH':
        street_name = '13TH'

    if street_name == 'FOURTEENTH':
        street_name = '14TH'

    if street_name == 'FIFTEENTH':
        street_name = '15TH'

    return ({
        'number': address_parts.get('AddressNumber', '').upper(),
        'directional': directional,
        'street_name': re.sub("'", "", street_name),
        'street_type': street_type,
        'city': city,
        'state': address_parts.get('StateName', '').upper(),
        'zip_code': zip_code,
    })


def geocode_from_address_parts(addr_parts, disambiguate=False):
    """
    :param addr_parts: dict of address par
    :return: Point representing location of address
    """

    # First try to get address point
    if disambiguate:
        point = geocode_address_point_distinguish(addr_parts)
        print("geocode_address_point_distinguish returned {}.".format(point))
    else:
        point = geocode_address_point(addr_parts)

    # If that fails, check parcel data
    if not point:
        if disambiguate:
            point = geocode_parcel_centroid_distinguish(addr_parts)
            print("geocode_parcel_centroid_distinguish returned {}.".format(point))
        else:
            point = geocode_parcel_centroid(addr_parts)
    return point

def geocode_from_address_string(addr_str, disambiguate = False):
    addr_parts = parse_address_string(addr_str)
    first_attempt = geocode_from_address_parts(addr_parts, disambiguate)
    print("    * first_attempt = " + str(first_attempt))
    if first_attempt is not None or not disambiguate:
        return first_attempt
    if addr_parts['directional'] in ['N', 'E', 'S', 'W']:
        # Since the first attempt didn't work, maybe it's one of those
        # cases where the cardinal direction is spelled out in the street_name
        # field instead of filed away in the directional field.
        print("    Trying again with the cardinal direction back in the street name.")
        addr_parts['street_name'] = cardinal_direction[addr_parts['directional']] + " " + addr_parts['street_name']
        addr_parts['directional'] = ''
        second_attempt = geocode_from_address_parts(addr_parts, disambiguate)
        if second_attempt is not None:
            return second_attempt

    # Maybe it's a case like 42A WHATEVER STREET, which should be
    # propertly formatted "42 WHATEVER STREET, APT A".
    if re.search('^\d+[a-zA-Z]$', addr_parts['number']) is not None:
        print("        Trying again after splitting off a letter from the address number.")
        addr_parts['number'] = addr_parts['number'][:-1]
        # Properly, the apartment designation should also be included somewhere
        # as it does actually figure in database matches in some cases.
        third_attempt = geocode_from_address_parts(addr_parts, disambiguate)
        if third_attempt is not None:
            return third_attempt

    # Or maybe it's a case like 42 A WHATEVER STREET, in which case
    # Parserator thinks that street_name == 'A WHATEVER', but it's
    # actually supposed to be the apartment letter.
    if re.search('^[A-DF-MO-RT-VX-Z] ', addr_parts['street_name']) is not None:
        print("            Trying again after splitting off the letter from the beginning of the street name.")
        addr_parts['street_name'] = re.sub('^[A-DF-MO-RT-VX-Z] ', '', addr_parts['street_name'])
        # Properly, the apartment designation should also be included somewhere
        # as it does actually figure in database matches in some cases.
        fourth_attempt = geocode_from_address_parts(addr_parts, disambiguate)
        if fourth_attempt is not None:
            return fourth_attempt

    return first_attempt

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

def try_to_pick_address(candidates):
    if len(candidates) == 1:
        return candidates[0].geom
    if len(candidates) > 1:
        municipalities = set([a.municipality for a in candidates])
        if len(municipalities) == 1:
            print("    Since they all have the same municipality, probably they are just apartments or sufficiently close variants, so return the geom of the first.")
            return candidates[0].geom
    return None

def geocode_address_point_distinguish(addr_parts):
    """A variant of geocode_address_point that tries hard to
    disambiguate similar results."""
    # first, try with zip
    addr = AddressPoint.objects.filter(
        address_number=addr_parts['number'],
        street_prefix=addr_parts['directional'],
        street_name__startswith=addr_parts['street_name'],
        street_type=addr_parts['street_type'],
        zip_code=addr_parts['zip_code']
    )
    print("    {} addresses found from first attempt.".format(len(addr))) #
    if len(addr) == 0:
        pprint(addr_parts)

    if len(addr) == 1:
        return addr[0].geom

    if len(addr) > 1:
        # Try to disambiguate by using the 'municipality' field from the table with
        # the 'city' field from the address.
        candidates = []
        for a in addr:
            print("a.municipality = {}, addr_parts['city'] = {}".format(a.municipality, addr_parts['city']))
            if a.municipality == addr_parts['city']:
                candidates.append(a)
        print("len(candidates) = {}".format(len(candidates)))
        selection = try_to_pick_address(candidates)
        if selection is not None:
            return selection
        elif len(candidates) == 0:
            print("This could be an indistinguishable postal city address.") # Why doesn't this get printed?

    # Try again with more lenient city search.
    addr = AddressPoint.objects.filter(
        address_number=addr_parts['number'],
        street_prefix=addr_parts['directional'],
        street_name__startswith=addr_parts['street_name'],
        street_type=addr_parts['street_type'],
        city__startswith=addr_parts['city']
    )
    selection = try_to_pick_address(addr)
    if selection is not None:
        return selection

    if len(addr) == 0: # Try to handle the case where the street_type is wrong by dropping it from the query.
        addr = AddressPoint.objects.filter(
            address_number=addr_parts['number'],
            street_prefix=addr_parts['directional'],
            street_name__startswith=addr_parts['street_name'],
            zip_code=addr_parts['zip_code']
        )

        selection = try_to_pick_address(addr)
        if selection is not None:
            return selection
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

def geocode_parcel_centroid_distinguish(addr_parts):
    """A variant of geocode_parcel_centroid that tries hard to
    disambiguate similar results."""
    street = addr_parts['street_name']
    if addr_parts['directional']:
        street = addr_parts['directional'] + ' ' + street
    city = addr_parts['city']

    parcels = Parcel.objects.filter(
        addr_number=addr_parts['number'],
        addr_street__startswith=street,
        addr_zip=zip
    )
    if len(parcels) == 1:
        return parcels[0].geom

    parcels = Parcel.objects.filter(
        addr_number=addr_parts['number'],
        addr_street__startswith=street,
        addr_city__startswith=city,
        addr_zip=zip
    )

    if len(parcels) == 1:
        return parcels[0].geom
    elif len(parcels) == 0:
        return None
    else:
        raise ValueError("Found {} parcels with the same house number ({}), starting characters for the street name ({}), city ({}) and ZIP code ({}).".format(addr_parts['number'], street, city, zip))

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

def forward_geocode(address, disambiguate=True):
    """
    Looks up geo data pertaining to `address`, but distinguish
    addresses with different cities.

    :param address:
    :return:
    """
    result = OD([('geom', {}), ('parcel_id', ''),
                 ('regions', {}), ('status', 'ERROR')])
    try:
        # get point
        point = geocode_from_address_string(address, disambiguate)
        if disambiguate and point is None:
            result['status'] = "Unable to geocode this address to a single unambigous point."
            return result
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
        elif len(parcels) == 1:
            parcel = parcels[0]
            result['status'] = 'OK'
        else:
            # Why are there multiple parcels here that contain the point?
            if not disambiguate:
                parcel = parcels[0]
                result['status'] = 'OK'
            else:
                result['status'] = "There are {} parcels that contain the point ({}, {}).".format(len(parcels), point.x, point.y)

        result['parcel_id'] = parcel.pin
    except:
        if not disambiguate:
            pass
        else:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Error: {}".format(exc_type))
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('!!! ' + line for line in lines))
            import re
            result['status'] = re.sub('\n', '|', ''.join('!!! ' + line for line in lines))
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
