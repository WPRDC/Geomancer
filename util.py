import psycopg2
import psycopg2.extras

import usaddress

import json

from .models import Parcel

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
    inner_qry = QRY_TEMPLATE.format(region_table=region_type, region_name=region_name)
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

    return f,m

def parse_coord_string(coord_string):
    x, y = coord_string.split(',')
    return float(x), float(y)

def parse_address_string(addr_str):
    address_parts, address_type = usaddress.tag(addr_str)

    # Get just first letter of Directional e.g. S from South Craig
    if 'StreetNamePreDirectional' in address_parts:
        directional = address_parts['StreetNamePreDirectional'][0] + ' '
    else:
        directional = ''

    number = address_parts.get('AddressNumber', '').upper()
    street = directional +  address_parts.get('StreetName', '').upper()
    street_type = address_parts.get('StreetNamePostType', '').upper()
    city = address_parts.get('PlaceName', '').upper()
    state = address_parts.get('StateName', '').upper()
    zip = address_parts.get('ZipCode','').upper()



    if address_type == 'Street Address':
        parcels = Parcel.objects.filter(
            addr_number=number,
            addr_street__startswith=street,
            addr_zip__contains=zip
        )
        return parcels

    else:
        return []