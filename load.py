from django.contrib.gis.utils import LayerMapping
from geoservices.models import *
import subprocess

SOURCE_DIR = "/home/sds25/projects/wprdc-tools/geoservices/source_data/"  #TODO: make relative

mapping = {
# "pittsburgh_neighborhood": {
#         "source": "pgh_hood/Pittsburgh_Neighborhoods.shp",
#         "model": "PghHood",
#         "mapping": {
#             "objectid": "objectid",
#             "fid_blockg": "fid_blockg",
#             "statefp10": "statefp10",
#             "countyfp10": "countyfp10",
#             "tractce10": "tractce10",
#             "blkgrpce10": "blkgrpce10",
#             "geoid10": "geoid10",
#             "namelsad10": "namelsad10",
#             "mtfcc10": "mtfcc10",
#             "funcstat10": "funcstat10",
#             "aland10": "aland10",
#             "awater10": "awater10",
#             "intptlat10": "intptlat10",
#             "intptlon10": "intptlon10",
#             "shape_leng": "shape_leng",
#             "fid_neighb": "fid_neighb",
#             "pghdbsdene": "pghdbsdeNe",
#             "perimeter": "perimeter",
#             "neighbor_field": "neighbor_",
#             "neighbor_i": "neighbor_i",
#             "hood": "hood",
#             "hood_no": "hood_no",
#             "acres": "acres",
#             "sqmiles": "sqmiles",
#             "dpwdiv": "dpwdiv",
#             "unique_id": "unique_id",
#             "sectors": "sectors",
#             "shape_le_1": "shape_le_1",
#             "shape_ar_1": "shape_ar_1",
#             "page_numbe": "page_numbe",
#             "plannerass": "plannerass",
#             "created_us": "created_us",
#             "created_da": "created_da",
#             "last_edite": "last_edite",
#             "last_edi_1": "last_edi_1",
#             "geom": "MULTIPOLYGON"
#         }
#     },
#     "pittsburgh_fire_zone": {
#         "source": "pgh_fire_zone/fire_zone.shp",
#         "model": "PghFireZone",
#         "mapping": {
#             "cartodb_id": "cartodb_id",
#             "firezones1": "firezones1",
#             "firezones_field": "firezones_",
#             "mapbook": "mapbook",
#             "olddist_zo": "olddist_zo",
#             "dist_zone": "dist_zone",
#             "shape_area": "shape_area",
#             "shape_leng": "shape_leng",
#             "perimeter": "perimeter",
#             "area": "area",
#             "dist": "dist",
#             "geom": "MULTIPOLYGON"
#         }
#     },
#     "pittsburgh_police_zone": {
#         "source": "pgh_police/Pittsburgh_Police_Zones.shp",
#         "model": "PghPoliceZone",
#         "mapping": {
#             "objectid": "objectid",
#             "perimeter": "perimeter",
#             "zone": "zone",
#             "geom": "MULTIPOLYGON"
#         }
#     },
#     "pittsburgh_ward": {
#         "source": "pgh_ward/wards.shp",
#         "model": "PghWard",
#         "mapping": {
#             "fid": "FID",
#             "area": "AREA",
#             "perimeter": "PERIMETER",
#             "wards_field": "WARDS_",
#             "wards_id": "WARDS_ID",
#             "ward": "WARD",
#             "acres": "ACRES",
#             "sqmiles": "SQMILES",
#             "unique_id": "UNIQUE_ID",
#             "council": "COUNCIL",
#             "dpw_insp": "DPW_INSP",
#             "shape_leng": "Shape_Leng",
#             "shape_area": "Shape_Area",
#             "geom": "MULTIPOLYGON"
#         }
#     },
#     "pittsburgh_city_council": {
#         "source": "pgh_city_council/Pittsburgh_City_Council_Districts.shp",
#         "model": "PghCityCouncil",
#         "mapping": {
#             "objectid_1": "objectid_1",
#             "objectid": "objectid",
#             "intptlat10": "intptlat10",
#             "intptlon10": "intptlon10",
#             "shape_leng": "shape_leng",
#             "council": "council",
#             "councilman": "councilman",
#             "committee": "committee",
#             "phone": "phone",
#             "geom": "MULTIPOLYGON"
#         }
#     },
#     "pittsburgh_dpw_division": {
#         "source": "pgh_dpw_division/Pittsburgh_DPW_Divisions.shp",
#         "model": "PghPublicWorks",
#         "mapping": {
#             "objectid": "objectid",
#             "pghdbsdedp": "pghdbsdeDP",
#             "perimeter": "perimeter",
#             "dpwdivs_field": "dpwdivs_",
#             "dpwdivs_id": "dpwdivs_id",
#             "sqmiles": "sqmiles",
#             "acres": "acres",
#             "division": "division",
#             "supervsr": "supervsr",
#             "unique_id": "unique_id",
#             "sq_miles": "sq_miles",
#             "dpw_divisi": "dpw_divisi",
#             "geom": "MULTIPOLYGON"
#         }
#     },
#     "allegheny_county_municipality": {
#         "source": "ac_municipalities/Allegheny_County_Municipal_Boundaries.shp",
#         "model": "ACMunicipality",
#         "mapping": {
#             "objectid": "OBJECTID",
#             "muni_name": "NAME",
#             "muni_type": "TYPE",
#             "label": "LABEL",
#             "cog": "COG",
#             "schoold": "SCHOOLD",
#             "congdist": "CONGDIST",
#             "fips": "FIPS",
#             "region": "REGION",
#             "acres": "ACRES",
#             "sqmi": "SQMI",
#             "municode": "MUNICODE",
#             "cntl_id": "CNTL_ID",
#             "cntycounci": "CNTYCOUNCI",
#             "eoc": "EOC",
#             "assessorte": "ASSESSORTE",
#             "valuationa": "VALUATIONA",
#             "yearconver": "YEARCONVER",
#             "globalid": "GlobalID",
#             "geom": "MULTIPOLYGON"
#         }
#     },
    "parcel": {
        "source": "parcels/untitled_table_24.shp",
        "model": "Parcel",
        "mapping": {
            "objectid": "objectid",
            "pin": "pin",
            "mapblocklot": "mapblocklo",
            "shapearea": "shapearea",
            "shapelen": "shapelen",
            "addr_number": "propertyho",
            "addr_fraction":"propertyfr",
            "addr_street":"propertyad",
            "addr_city":"propertyci",
            "addr_state":"propertyst",
            "addr_unit":"propertyun",
            "addr_zip":"propertyzi",
            "geom": "MULTIPOLYGON"
        }
    },
    # "block_group":{
    #     "source": "block_groups/cb_2016_42_bg_500k.shp",
    #     "model": "BlockGroup",
    #     "source_srs": 4269,
    #     "mapping": {
    #         "geo_id": "GEOID",
    #         "state": "STATEFP",
    #         "county": "COUNTYFP",
    #         "tract": "TRACTCE",
    #         "block_grp": "BLKGRPCE",
    #         "geom": "MULTIPOLYGON"
    #     }
    # }
}


def run(verbose=True):
    global mapping
    subprocess.run(['psql', 'django', '-c', 'TRUNCATE parcels'])


    for title, data in mapping.items():
        print(title)

        table = "geoservices_" + data['model'].lower()

        subprocess.run(['psql', 'django', '-c', 'truncate '+ table])

        shp = SOURCE_DIR + data['source']
        mapping = data['mapping']
        model = globals()[data['model']]
        lm = LayerMapping(
            model, shp, mapping,
            transform=False, encoding='iso-8859-1',
        )
        lm.save(strict=True, verbose=verbose)