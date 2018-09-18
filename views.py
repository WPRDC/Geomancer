from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.contrib.gis.geos import Point
from django.forms.models import model_to_dict

from wprdc_tools import settings
from collections import OrderedDict

import json
import csv

from .models import *
from .util import parse_options, parse_coord_string, parse_address_string, geocode_file, geocode_from_address_string, forward_geocode, spatial_query
from .forms import GeoserviceFileForm


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
            r = [{'id': region.id, 'name': region.name,
                  'description': region.description} for region in regions]

            response = {**BASE_RESPONSE, **
                        {'status': 'OK', 'results': r, 'help': ''}}

        else:
            # List names of regions of type specified in `region_type`
            r_type = RegionType.objects.get(pk=region_type)
            regions = AdminRegion.objects.filter(type=r_type)

            if fmt == 'geojson':
                geo = serialize('geojson', regions, geometry_field='geom')
                results = json.loads(geo)
                response = {**BASE_RESPONSE, **
                            {'status': 'OK', 'results': results, 'help': ''}}
            else:
                results = [{'id': region.name, 'name': region.title}
                           for region in regions]
                response = {**BASE_RESPONSE, **
                            {'status': 'OK', 'results': results, 'help': ''}}
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
        r = [{'id': region.id, 'name': region.name,
              'description': region.description} for region in regions]

        response = {**BASE_RESPONSE, **
                    {'status': 'OK', 'results': r, 'help': ''}}
        status = 200
    except:
        if settings.DEBUG:
            raise
        else:
            # TODO: error handling and modify resposne accordingly
            response = BASE_RESPONSE
            status = 400

    return (JsonResponse(response, status=status))


def parcels_in_old(request, region_type="", region_name=""):
    '''

    :param request:
    :param region_type:
    :param region_name:
    :return:
    '''
    download = False  # flag to set to server results as file download
    response = BASE_RESPONSE
    print('parcels in old')

    if 'format' in request.GET:
        if request.GET['format'] == 'file':
            download = True

    try:
        region = AdminRegion.objects.filter(
            type=region_type, name=region_name)[0]
        parcels = Parcel.objects.filter(geom__intersects=region.geom)
        shp = serialize('geojson', parcels, geometry_field='geom')
        if (download):
            response = HttpResponse(
                shp, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s.geojson' % region_name
            response.write(shp)
            return response
        else:
            return JsonResponse(json.loads(shp))
    except:
        return JsonResponse(response, status=400)


def parcels_in(request, region_type="", region_name=""):
    '''

    :param request:
    :param region_type:
    :param region_name:
    :return:
    '''
    # Set result format
    fmt, mthd = parse_options(request.GET)
    print(fmt, mthd)
    try:
        # Find region and filter parcels within that region
        region = AdminRegion.objects.filter(
            type=region_type, name=region_name)[0]
        parcels = Parcel.objects.filter(geom__intersects=region.geom)

        # If downloading serve geojson file
        if (mthd == 'download'):
            # Serialize QuerySet of parcels to geojson
            shp = serialize('geojson', parcels, geometry_field='geom')

            response = HttpResponse(
                shp, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s.geojson' % region_name
            response.write(shp)
            return response

        # If not downloading...
        else:
            if fmt == 'geojson':
                shp = serialize('geojson', parcels, geometry_field='geom')
                response = {**BASE_RESPONSE, **{'status': 'OK',
                                                'help': '', 'results': json.loads(shp)}}
            else:
                l = [parcel.pin for parcel in parcels]
                response = {**BASE_RESPONSE, **
                            {'status': 'OK', 'help': '', 'results': l}}
            return JsonResponse(response)
    except:
        if settings.DEBUG:
            raise
        else:
            # TODO: error handling and modify resposne accordingly
            return (JsonResponse(BASE_RESPONSE, status=400))


def reverse_geocode(request):
    '''

    :param request:
    :param x:
    :param y:
    :param pin:
    :param srid:
    :param region_types:
    :return:
    '''
    pnt = None
    response = {}
    status = 400
    srid = 4326

    if request.method == 'GET':
        x = request.GET.get('lng', None)
        y = request.GET.get('lat', None)
        pin = request.GET.get('pin', None)
        srid = request.GET.get('srid', None)
        regions_list = request.GET.get('regions', '')

        # Shorthand params
        if not x:
            x = request.GET.get('x', None)
        if not y:
            y = request.GET.get('y', None)
        if not pin:
            pin = request.GET.get('p', None)
        if not srid:
            srid = request.GET.get('s', 4326)
        if not regions_list:
            regions_list = request.GET.get('r', '')

        if regions_list:
            regions_list = regions_list.split(',')

        if pin:
            parcel = Parcel.objects.get(pin=pin)
            pnt = parcel.geom.centroid
        elif x != None and y != None:
            try:
                pnt = Point(x=float(x), y=float(y), srid=srid)
            except:
                response = {**BASE_RESPONSE,
                            **{'status': 'ERR', 'results': '',
                               'help': 'Lat and lng must be in decimal format'}}
        else:
            response = {**BASE_RESPONSE,
                        **{'status': 'ERR', 'results': '',
                           'help': 'Coordinates (x/lng & y/lat) or parcel id (PIN) required'}}

        if pnt:
            if regions_list:
                regions = AdminRegion.objects.filter(
                    type__in=regions_list, geom__contains=pnt)
            else:
                regions = AdminRegion.objects.filter(geom__contains=pnt)

            results = {region.type.id: {'id': region.name,
                                        'name': region.title} for region in regions}
            response = {**BASE_RESPONSE, **
                        {'status': 'OK', 'results': results}}
            status = 200
            if not results.keys():
                response = {**BASE_RESPONSE, **
                        {'status': 'WARNING', 'help': 'Location out of range', 'results': None}}
                status = 204

    else:
        # Wrong request method
        response = {**BASE_RESPONSE, **{'status': 'ERR', 'results': '',
                                        'help': '"{}" not supported for this view.'.format(request.method)}}

    return JsonResponse(response, status=status)


def geocode(request):
    addr = request.GET['addr']
    response = {'data': {}}

    response['data'] = forward_geocode(addr)

    return JsonResponse(response, status=200)


def address_search(request):
    upload_form = GeoserviceFileForm
    return render(request, 'geocoder/address_search.html', {'upload_form': upload_form})


def upload_file(request):
    if request.method == 'POST':
        form = GeoserviceFileForm(request.POST, request.FILES)
        if form.is_valid():
            stuff = form.save()
            file = stuff.file
            new_data, fields = geocode_file(
                stuff.file.url, stuff.address_field)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="geocoded_data.csv"'

            writer = csv.DictWriter(response, fieldnames=fields)
            writer.writeheader()
            writer.writerows(new_data)

            return response
        else:
            return JsonResponse({'status': 'not OK'})

    else:
        return JsonResponse({'status': 'not OK'})


def spatial_query_object(request, region_type="", region_name=""):
    '''
    Retrieve data for regions that intersect target region
    :param request:
    :param region_type:
    :param region_name:
    :return:
    '''
    SPATIAL_QUERIES = ['intersects', 'within', 'overlaps', 'crosses', 'covers',
                       'coveredby', 'contains', 'disjoint', 'touches',
                       'bbcontains']

    method = request.GET.get('method', 'intersects')
    if method not in SPATIAL_QUERIES:
        return JsonResponse(
            {
                **BASE_RESPONSE,
                **{'help': '{} is not a suppoorted method. Use one of the following `{}`'.format(method, '`,`'.join(SPATIAL_QUERIES))}
            }, status=400)

    try:
        data = spatial_query(region_type, region_name, method)

        response = {
            **BASE_RESPONSE,
            **{'status': 'OK', 'help': '', 'results': data}
        }
        return JsonResponse(response)
    except Exception:
        if settings.DEBUG:
            raise
        else:
            return (JsonResponse(BASE_RESPONSE, status=400))
