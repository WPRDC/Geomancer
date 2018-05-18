MODEL_MAPPING = {
    "pittsburgh_neighborhood": {
        "url": "",
        "source": "pgh_hood/Pittsburgh_Neighborhoods.shp",
        "model": "PghHood",
        "mapping": {
            "objectid": "objectid",
            "fid_blockg": "fid_blockg",
            "statefp10": "statefp10",
            "countyfp10": "countyfp10",
            "tractce10": "tractce10",
            "blkgrpce10": "blkgrpce10",
            "geoid10": "geoid10",
            "namelsad10": "namelsad10",
            "mtfcc10": "mtfcc10",
            "funcstat10": "funcstat10",
            "aland10": "aland10",
            "awater10": "awater10",
            "intptlat10": "intptlat10",
            "intptlon10": "intptlon10",
            "shape_leng": "shape_leng",
            "fid_neighb": "fid_neighb",
            "pghdbsdene": "pghdbsdeNe",
            "perimeter": "perimeter",
            "neighbor_field": "neighbor_",
            "neighbor_i": "neighbor_i",
            "hood": "hood",
            "hood_no": "hood_no",
            "acres": "acres",
            "sqmiles": "sqmiles",
            "dpwdiv": "dpwdiv",
            "unique_id": "unique_id",
            "sectors": "sectors",
            "shape_le_1": "shape_le_1",
            "shape_ar_1": "shape_ar_1",
            "page_numbe": "page_numbe",
            "plannerass": "plannerass",
            "created_us": "created_us",
            "created_da": "created_da",
            "last_edite": "last_edite",
            "last_edi_1": "last_edi_1",
            "geom": "MULTIPOLYGON"
        }
    },
    "pittsburgh_fire_zone": {
        "source": "pgh_fire_zone/fire_zone.shp",
        "model": "PghFireZone",
        "mapping": {
            "cartodb_id": "cartodb_id",
            "firezones1": "firezones1",
            "firezones_field": "firezones_",
            "mapbook": "mapbook",
            "olddist_zo": "olddist_zo",
            "dist_zone": "dist_zone",
            "shape_area": "shape_area",
            "shape_leng": "shape_leng",
            "perimeter": "perimeter",
            "area": "area",
            "dist": "dist",
            "geom": "MULTIPOLYGON"
        }
    },
    "pittsburgh_police_zone": {
        "source": "pgh_police/Pittsburgh_Police_Zones.shp",
        "model": "PghPoliceZone",
        "mapping": {
            "objectid": "objectid",
            "perimeter": "perimeter",
            "zone": "zone",
            "geom": "MULTIPOLYGON"
        }
    },
    "pittsburgh_ward": {
        "source": "pgh_ward/wards.shp",
        "model": "PghWard",
        "mapping": {
            "fid": "FID",
            "area": "AREA",
            "perimeter": "PERIMETER",
            "wards_field": "WARDS_",
            "wards_id": "WARDS_ID",
            "ward": "WARD",
            "acres": "ACRES",
            "sqmiles": "SQMILES",
            "unique_id": "UNIQUE_ID",
            "council": "COUNCIL",
            "dpw_insp": "DPW_INSP",
            "shape_leng": "Shape_Leng",
            "shape_area": "Shape_Area",
            "geom": "MULTIPOLYGON"
        }
    },
    "pittsburgh_city_council": {
        "source": "pgh_city_council/Pittsburgh_City_Council_Districts.shp",
        "model": "PghCityCouncil",
        "mapping": {
            "objectid_1": "objectid_1",
            "objectid": "objectid",
            "intptlat10": "intptlat10",
            "intptlon10": "intptlon10",
            "shape_leng": "shape_leng",
            "council": "council",
            "councilman": "councilman",
            "committee": "committee",
            "phone": "phone",
            "geom": "MULTIPOLYGON"
        }
    },
    "pittsburgh_dpw_division": {
        "source": "pgh_dpw_division/Pittsburgh_DPW_Divisions.shp",
        "model": "PghPublicWorks",
        "mapping": {
            "objectid": "objectid",
            "pghdbsdedp": "pghdbsdeDP",
            "perimeter": "perimeter",
            "dpwdivs_field": "dpwdivs_",
            "dpwdivs_id": "dpwdivs_id",
            "sqmiles": "sqmiles",
            "acres": "acres",
            "division": "division",
            "supervsr": "supervsr",
            "unique_id": "unique_id",
            "sq_miles": "sq_miles",
            "dpw_divisi": "dpw_divisi",
            "geom": "MULTIPOLYGON"
        }
    },
    "allegheny_county_municipality": {
        "source": "ac_municipalities/Allegheny_County_Municipal_Boundaries.shp",
        "model": "ACMunicipality",
        "mapping": {
            "objectid": "OBJECTID",
            "muni_name": "NAME",
            "muni_type": "TYPE",
            "label": "LABEL",
            "cog": "COG",
            "schoold": "SCHOOLD",
            "congdist": "CONGDIST",
            "fips": "FIPS",
            "region": "REGION",
            "acres": "ACRES",
            "sqmi": "SQMI",
            "municode": "MUNICODE",
            "cntl_id": "CNTL_ID",
            "cntycounci": "CNTYCOUNCI",
            "eoc": "EOC",
            "assessorte": "ASSESSORTE",
            "valuationa": "VALUATIONA",
            "yearconver": "YEARCONVER",
            "globalid": "GlobalID",
            "geom": "MULTIPOLYGON"
        }
    },
    "block_group": {
        "source": "block_groups/Allegheny_County_Census_Block_Groups_2016.shp",
        "model": "BlockGroup",
        "mapping": {
            "fid": "FID",
            "state": "STATEFP",
            "county": "COUNTYFP",
            "tract": "TRACTCE",
            "block_grp": "BLKGRPCE",
            "geom": "MULTIPOLYGON"
        }
    },
    "census_tract": {
        "source": "census_tracts/Allegheny_County_Census_Tracts_2016.shp",
        "model": "CensusTract",
        "mapping": {
            "geo_id": "GEOID",
            "state": "STATEFP",
            "county": "COUNTYFP",
            "tract": "TRACTCE",
            "lsad": "LSAD",
            "geom": "MULTIPOLYGON"
        }
    },
    "census_block": {
        "source": "census_blocks/Allegheny_County_Census_Blocks_2016.shp",
        "model": "CensusBlock",
        "mapping": {
            "fid": "FID",
            "state": "STATEFP10",
            "county": "COUNTYFP10",
            "tract": "TRACTCE10",
            "block": "BLOCKCE10",
            "geom": "MULTIPOLYGON"
        }
    },
    "school_district": {
        "source": "school_dist/Allegheny_County_School_District_Boundaries.shp",
        "model": "SchoolDistrict",
        "mapping": {
            "object_id": "OBJECTID",
            "district_name": "SCHOOLD",
            "geom": "MULTIPOLYGON"
        }
    },
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
            "addr_fraction": "propertyfr",
            "addr_street": "propertyad",
            "addr_city": "propertyci",
            "addr_state": "propertyst",
            "addr_unit": "propertyun",
            "addr_zip": "propertyzi",
            "geom": "MULTIPOLYGON"
        }
    },

    "address": {
        "source": "ac_address_points/Allegheny_County_Address_Points.shp",
        "model": "AddressPoint",
        "mapping": {
            "object_id": "OBJECTID",
            "address_id": "ADDRESS_ID",
            "street_id": "STREET_ID",
            "dup_street_id": "DUP_STREET",
            "address_type": "ADDRESS_TY",
            "full_address": "FULL_ADDRE",
            "address_number_prefix": "ADDR_NUM_P",
            "address_number": "ADDR_NUM",
            "address_number_suffix": "ADDR_NUM_S",
            "street_premodifier": "ST_PREMODI",
            "street_prefix": "ST_PREFIX",
            "street_pretype": "ST_PRETYPE",
            "street_name": "ST_NAME",
            "street_type": "ST_TYPE",
            "street_postmodifier": "ST_POSTMOD",
            "unit": "UNIT",
            "unit_type": "UNIT_TYPE",
            "floor": "FLOOR",
            "municipality": "MUNICIPALI",
            "county": "COUNTY",
            "state": "STATE",
            "zip_code": "ZIP_CODE",
            "zip_code_four": "ZIP_CODE4",
            "comment": "COMMENT",
            "edit_date": "EDIT_DATE",
            "source": "SOURCE",
            "geom": "POINT"
        }
    }
}

ZIP_MAPPING = {
    "15003": {
        "NAME": "AMBRIDGE"
    },
    "15005": {
        "NAME": "BADEN"
    },
    "15006": {
        "NAME": "BAIRDFORD"
    },
    "15007": {
        "NAME": "BAKERSTOWN"
    },
    "15014": {
        "NAME": "BRACKENRIDGE"
    },
    "15015": {
        "NAME": "BRADFORD WOODS"
    },
    "15017": {
        "NAME": "BRIDGEVILLE"
    },
    "15018": {
        "NAME": "BUENA VISTA"
    },
    "15020": {
        "NAME": "BUNOLA"
    },
    "15024": {
        "NAME": "CHESWICK"
    },
    "15025": {
        "NAME": "CLAIRTON"
    },
    "15026": {
        "NAME": "CLINTON"
    },
    "15028": {
        "NAME": "COULTERS"
    },
    "15030": {
        "NAME": "CREIGHTON"
    },
    "15031": {
        "NAME": "CUDDY"
    },
    "15034": {
        "NAME": "DRAVOSBURG"
    },
    "15035": {
        "NAME": "EAST MC KEESPORT"
    },
    "15037": {
        "NAME": "ELIZABETH"
    },
    "15044": {
        "NAME": "GIBSONIA"
    },
    "15045": {
        "NAME": "GLASSPORT"
    },
    "15046": {
        "NAME": "CRESCENT"
    },
    "15047": {
        "NAME": "GREENOCK"
    },
    "15049": {
        "NAME": "HARWICK"
    },
    "15051": {
        "NAME": "INDIANOLA"
    },
    "15056": {
        "NAME": "LEETSDALE"
    },
    "15057": {
        "NAME": "MC DONALD"
    },
    "15063": {
        "NAME": "MONONGAHELA"
    },
    "15064": {
        "NAME": "MORGAN"
    },
    "15065": {
        "NAME": "NATRONA HEIGHTS"
    },
    "15068": {
        "NAME": "NEW KENSINGTON"
    },
    "15071": {
        "NAME": "OAKDALE"
    },
    "15075": {
        "NAME": "RURAL RIDGE"
    },
    "15076": {
        "NAME": "RUSSELLTON"
    },
    "15082": {
        "NAME": "STURGEON"
    },
    "15083": {
        "NAME": "SUTERSVILLE"
    },
    "15084": {
        "NAME": "TARENTUM"
    },
    "15085": {
        "NAME": "TRAFFORD"
    },
    "15086": {
        "NAME": "WARRENDALE"
    },
    "15088": {
        "NAME": "WEST ELIZABETH"
    },
    "15089": {
        "NAME": "WEST NEWTON"
    },
    "15090": {
        "NAME": "WEXFORD"
    },
    "15101": {
        "NAME": "ALLISON PARK"
    },
    "15102": {
        "NAME": "BETHEL PARK"
    },
    "15104": {
        "NAME": "BRADDOCK"
    },
    "15106": {
        "NAME": "CARNEGIE"
    },
    "15108": {
        "NAME": "CORAOPOLIS"
    },
    "15110": {
        "NAME": "DUQUESNE"
    },
    "15112": {
        "NAME": "EAST PITTSBURGH"
    },
    "15116": {
        "NAME": "GLENSHAW"
    },
    "15120": {
        "NAME": "HOMESTEAD"
    },
    "15122": {
        "NAME": "WEST MIFFLIN"
    },
    "15126": {
        "NAME": "IMPERIAL"
    },
    "15129": {
        "NAME": "SOUTH PARK"
    },
    "15131": {
        "NAME": "MCKEESPORT"
    },
    "15132": {
        "NAME": "MCKEESPORT"
    },
    "15133": {
        "NAME": "MCKEESPORT"
    },
    "15135": {
        "NAME": "MCKEESPORT"
    },
    "15136": {
        "NAME": "MC KEES ROCKS"
    },
    "15137": {
        "NAME": "NORTH VERSAILLES"
    },
    "15139": {
        "NAME": "OAKMONT"
    },
    "15140": {
        "NAME": "PITCAIRN"
    },
    "15142": {
        "NAME": "PRESTO"
    },
    "15143": {
        "NAME": "SEWICKLEY"
    },
    "15144": {
        "NAME": "SPRINGDALE"
    },
    "15145": {
        "NAME": "TURTLE CREEK"
    },
    "15146": {
        "NAME": "MONROEVILLE"
    },
    "15147": {
        "NAME": "VERONA"
    },
    "15148": {
        "NAME": "WILMERDING"
    },
    "15201": {
        "NAME": "PITTSBURGH"
    },
    "15202": {
        "NAME": "PITTSBURGH"
    },
    "15203": {
        "NAME": "PITTSBURGH"
    },
    "15204": {
        "NAME": "PITTSBURGH"
    },
    "15205": {
        "NAME": "PITTSBURGH"
    },
    "15206": {
        "NAME": "PITTSBURGH"
    },
    "15207": {
        "NAME": "PITTSBURGH"
    },
    "15208": {
        "NAME": "PITTSBURGH"
    },
    "15209": {
        "NAME": "PITTSBURGH"
    },
    "15210": {
        "NAME": "PITTSBURGH"
    },
    "15211": {
        "NAME": "PITTSBURGH"
    },
    "15212": {
        "NAME": "PITTSBURGH"
    },
    "15213": {
        "NAME": "PITTSBURGH"
    },
    "15214": {
        "NAME": "PITTSBURGH"
    },
    "15215": {
        "NAME": "PITTSBURGH"
    },
    "15216": {
        "NAME": "PITTSBURGH"
    },
    "15217": {
        "NAME": "PITTSBURGH"
    },
    "15218": {
        "NAME": "PITTSBURGH"
    },
    "15219": {
        "NAME": "PITTSBURGH"
    },
    "15220": {
        "NAME": "PITTSBURGH"
    },
    "15221": {
        "NAME": "PITTSBURGH"
    },
    "15222": {
        "NAME": "PITTSBURGH"
    },
    "15223": {
        "NAME": "PITTSBURGH"
    },
    "15224": {
        "NAME": "PITTSBURGH"
    },
    "15225": {
        "NAME": "PITTSBURGH"
    },
    "15226": {
        "NAME": "PITTSBURGH"
    },
    "15227": {
        "NAME": "PITTSBURGH"
    },
    "15228": {
        "NAME": "PITTSBURGH"
    },
    "15229": {
        "NAME": "PITTSBURGH"
    },
    "15232": {
        "NAME": "PITTSBURGH"
    },
    "15233": {
        "NAME": "PITTSBURGH"
    },
    "15234": {
        "NAME": "PITTSBURGH"
    },
    "15235": {
        "NAME": "PITTSBURGH"
    },
    "15236": {
        "NAME": "PITTSBURGH"
    },
    "15237": {
        "NAME": "PITTSBURGH"
    },
    "15238": {
        "NAME": "PITTSBURGH"
    },
    "15239": {
        "NAME": "PITTSBURGH"
    },
    "15241": {
        "NAME": "PITTSBURGH"
    },
    "15243": {
        "NAME": "PITTSBURGH"
    },
    "15261": {
        "NAME": "PITTSBURGH"
    },
    "15275": {
        "NAME": "PITTSBURGH"
    },
    "15276": {
        "NAME": "PITTSBURGH"
    },
    "15282": {
        "NAME": "PITTSBURGH"
    },
    "15290": {
        "NAME": "PITTSBURGH"
    },
    "15321": {
        "NAME": "CECIL"
    },
    "15332": {
        "NAME": "FINLEYVILLE"
    },
    "15642": {
        "NAME": "IRWIN"
    },
    "15668": {
        "NAME": "MURRYSVILLE"
    },
    "16046": {
        "NAME": "MARS"
    },
    "16055": {
        "NAME": "SARVER"
    },
    "16056": {
        "NAME": "SAXONBURG"
    },
    "16059": {
        "NAME": "VALENCIA"
    },
    "16229": {
        "NAME": "FREEPORT"
    }
}
