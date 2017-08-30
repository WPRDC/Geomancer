from django.conf.urls import url

from . import views

# REGEX FOR COORDINATE STRING: (?P<coord_string>(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?))


api_urls = [
    url(r'^api/v0/parcels_in/(?P<region_type>[\w-]+)/(?P<region_name>[\w-]+)/$', views.parcels_in, name='v0_parcels_in'),
    url(r'^api/v0/regions/$', views.region_types, name='v0_regions_types'),
    url(r'^api/v0/regions/(?P<region_type>[\w-]+)/$', views.regions, name='v0_regions'),
    url(r'^api/v0/reverse_geocode/$', views.reverse_geocode, name='v0_reverse_geocode'),
    url(r'^api/v0/geocode/$', views.geocode, name='v0_geocode'),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^parcels_in/(?P<region_type>[\w-]+)/(?P<region_name>[\w-]+)/$', views.parcels_in_old, name='parcels_in_old'),

    url(r'^regions/$', views.region_types, name='regions_types'),
    url(r'^regions/(?P<region_type>[\w-]+)/$', views.regions, name='regions'),

    url(r'^reverse_geocode/$', views.reverse_geocode, name='reverse_geocode'),
    url(r'^geocode/$', views.geocode, name='geocode'),
    url(r'^address_search/$', views.address_search, name='addr_search'),

    url(r'^upload/$', views.upload_file, name="file_upload")
] + api_urls