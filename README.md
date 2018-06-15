# Geomancer v0.1
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A set of GIS services for geographical data hosted on the [Western Pennsylvania Regional Data Center](https://wprdc.org).  
Our current instance can be found at [https://tools.wprdc.org/geo/](https://tools.wprdc.org/geo/)


## Services
1. [Regions](#regions)
2. [Geocoder](#geocoder)
3. [Reverse Geocoder](#reverse-geocoder)
4. [Parcels-in](#parcels-in)


### Regions `/regions/`  `/regions/<region_type>`  
Lists administrative region types and regions. If no `region_type` is provided, a list of `region_type`s will be returned.
#### Example
`GET .../regions/`
```json
{
  "help": "",
  "results": [
    {
      "name": "Pittsburgh Ward",
      "id": "pittsburgh_ward",
      "description": "Pittsburgh wards"
    },
    {
      "name": "Pittsburgh Police Zone",
      "id": "pittsburgh_police_zone",
      "description": "police zones in Pittsburgh"
    },
    {
      "name": "Pittsburgh Neighborhood",
      "id": "pittsburgh_neighborhood",
      "description": "Neighborhoods in Pittsburgh"
    }
    //...
  ],
  "status": "OK"
}
```

`GET .../regions/pittsburgh_neighborhood`
```json
{
  "help": "",
  "results": [
    {
      "name": "Beltzhoover",
      "id": "beltzhoover"
    },
    {
      "name": "South Side Flats",
      "id": "south_side_flats"
    },
    {
      "name": "Allentown",
      "id": "allentown"
    },
    {
      "name": "Mount Washington",
      "id": "mount_washington"
    }
    //...
  ],
  "status": "OK"
}
```


### Geocoder
Maps a street address to latitude and longitude.

#### Required Paramaters
* `addr` - address to geocode (required)
#### Example
`GET .../geocode?addr=3343 Forbes Ave Pittsburgh PA 15213`
```json
{
  "data": {
    "geom": {
      "coordinates": [
        -79.9618888879302,
        40.438345724999
      ],
      "type": "Point"
    },
    "parcel_id": "0028F00193000000",
    "regions": {
      "pittsburgh_ward": {
        "name": "4",
        "id": "4"
      },
      "allegheny_county_municipality": {
        "name": "Pittsburgh",
        "id": "pittsburgh"
      },
      "pittsburgh_fire_zone": {
        "name": "2-14",
        "id": "2_14"
      },
      "pittsburgh_police_zone": {
        "name": "4",
        "id": "4"
      },
      "pittsburgh_dpw_division": {
        "name": "3",
        "id": "3"
      },
      "pittsburgh_neighborhood": {
        "name": "South Oakland",
        "id": "south_oakland"
      },
      "us_block_group": {
        "name": "420030409001",
        "id": "420030409001"
      },
      "pittsburgh_city_council": {
        "name": "6",
        "id": "6"
      }
    },
    "status": "OK"
  }
}
````



### Reverse Geocoder  
#### Required Parameters
* `lat` - latitude of target location
* `lng` - longitude of target location  
*OR*
* `pin` - parcel ID of target parcel

#### Option Parameters
* `srid` - [Spatial Reference System Identifier](https://en.wikipedia.org/wiki/Spatial_reference_system) - default: `4326`
* `regions_list` - list of `region_type`s for limiting results. (available `region_type`s can be found using [`Regions`](#regions) endpoint.

#### Example
`GET .../reverse_geocode/?lat=40.44301069&lng=-80.00475374`
```json
{
  "status": "OK",
  "help": "",
  "results": {
    "pittsburgh_dpw_division": {
      "id": "6",
      "name": "6"
    },
    "pittsburgh_fire_zone": {
      "id": "1_3",
      "name": "1-3"
    },
    "pittsburgh_ward": {
      "id": "2",
      "name": "2"
    },
    "pittsburgh_neighborhood": {
      "id": "central_business_district",
      "name": "Central Business District"
    },
    "us_block_group": {
      "id": "420030201002",
      "name": "420030201002"
    },
    "pittsburgh_police_zone": {
      "id": "2",
      "name": "2"
    },
    "pittsburgh_city_council": {
      "id": "6",
      "name": "6"
    },
    "allegheny_county_municipality": {
      "id": "pittsburgh",
      "name": "Pittsburgh"
    }
  }
}
```
### Parcels-in `/parcels-in/<region_type>/<region_id>`  
Returns a list of parcel IDs for parcels that fall within the requested region.

#### Example
`GET .../parcels-in/pittsburgh_ward/1/`
```json
{
  "help": "",
  "results": [
    "0002M00211000C00",
    "0002M00214000B00",
    "0011J00091000000",
    "0011J00154000000",
    "0001M00018000000",
    "0002M00070000000"
    //...
  ],
  "status": "OK"
}
```
### Spatial Query `/spatial-query/<region_type>/<region_id>`  
Returns a list of parcel IDs for parcels that fall within the requested region.

#### Example
`GET .../parcels-/pittsburgh_ward/1/`
```json
{
  "help": "",
  "results": [
    "0002M00211000C00",
    "0002M00214000B00",
    "0011J00091000000",
    "0011J00154000000",
    "0001M00018000000",
    "0002M00070000000"
    //...
  ],
  "status": "OK"
}
```
