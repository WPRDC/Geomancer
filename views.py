from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.contrib.gis.geos import Point
from django.forms.models import model_to_dict

from wprdc_tools import settings
from collections import OrderedDict
import json

from .models import *
from .util import parse_options, parse_coord_string

BASE_RESPONSE = OrderedDict(
    (
        ('status', 'Error'),
        ('results', None),
        ('help', 'Help text to come.'),
    )
)


# Create your views here.
def index(request):
    return render(request, 'geocoder/index.html')


def regions(request, region_type=""):
    '''
    
    :param request: 
    :param region_type: 
    :return: 
    '''
    fmt, mthd = parse_options(request.GET)
    try:
        if not region_type:
            # List available region types (neighborhood, municipality, various districts)
            regions = RegionType.objects.all()
            r = [{'id': region.id, 'name': region.name, 'description': region.description} for region in regions]

            response = {**BASE_RESPONSE, **{'status': 'OK', 'results': r, 'help': ''}}

        else:
            # List names of regions of type specified in `region_type`
            r_type = RegionType.objects.get(pk=region_type)
            regions = AdminRegion.objects.filter(type=r_type)

            if fmt == 'geojson':
                geo = serialize('geojson', regions, geometry_field='geom')
                results = json.loads(geo)
                response = {**BASE_RESPONSE, **{'status': 'OK', 'results': results, 'help': ''}}
            else:
                results = [{'id': region.name, 'name': region.title} for region in regions]
                response = {**BASE_RESPONSE, **{'status': 'OK', 'results': results, 'help': ''}}
        status = 200

    except:
        if settings.DEBUG:
            raise
        else:
            response = BASE_RESPONSE
            status = 400

    return JsonResponse(response, status=status)


def region_types(request):
    try:
        # List available region types (neighborhood, municipality, various districts)
        regions = RegionType.objects.all()
        r = [{'id': region.id, 'name': region.name, 'description': region.description} for region in regions]

        response = {**BASE_RESPONSE, **{'status': 'OK', 'results': r, 'help': ''}}
        status = 200
    except:
        if settings.DEBUG:
            raise
        else:
            # TODO: error handling and modify resposne accordingly
            response = BASE_RESPONSE
            status = 400

    return (JsonResponse(response, status=status))


def parcels_in(request, region_type="", region_name=""):
    '''
    
    :param request: 
    :param region_type: 
    :param region_name: 
    :return: 
    '''
    # Set result format
    fmt, mthd = parse_options(request.GET)

    try:
        # Find region and filter parcels within that region
        region = AdminRegion.objects.filter(type=region_type, name=region_name)[0]
        parcels = Parcel.objects.filter(geom__intersects=region.geom)

        # If downloading serve geojson file
        if (mthd == 'download'):
            # Serialize QuerySet of parcels to geojson
            shp = serialize('geojson', parcels, geometry_field='geom')

            response = HttpResponse(shp, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s.geojson' % region_name
            response.write(shp)
            return response

        # If not downloading...
        else:
            if fmt == 'geojson':
                shp = serialize('geojson', parcels, geometry_field='geom')
                response = {**BASE_RESPONSE, **{'status': 'OK', 'help': '', 'results': json.loads(shp)}}
            else:
                l = [parcel.pin for parcel in parcels]
                response = {**BASE_RESPONSE, **{'status': 'OK', 'help': '', 'results': l}}
            return JsonResponse(response)
    except:
        if settings.DEBUG:
            raise
        else:
            # TODO: error handling and modify resposne accordingly
            return (JsonResponse(BASE_RESPONSE, status=400))


def reverse_geocode(request, coord_string, srid=4326, region_types=''):
    try:
        lng, lat = parse_coord_string(coord_string)
        pnt = Point(lng, lat, srid=srid)
        if region_types:
            region_types=region_types.split(',')
            regions = AdminRegion.objects.filter(type__in=region_types, geom__contains=pnt)
        else:
            regions = AdminRegion.objects.filter(geom__contains=pnt)

        results = {region.type.id: {'id': region.name, 'name': region.title} for region in regions}
        response = {**BASE_RESPONSE, **{'status': 'OK', 'results': results}}

        status = 200
    except:
        if settings.DEBUG:
            raise
        else:
            response = BASE_RESPONSE
            status = 400
    print(json.dumps(response))
    return JsonResponse(response, status=status)