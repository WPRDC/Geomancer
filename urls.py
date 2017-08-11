from django.conf.urls import url

from . import views

# REGEX FOR COORDINATE STRING: (?P<coord_string>(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?))


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^parcels_in/(?P<region_type>[\w-]+)/(?P<region_name>[\w-]+)/$', views.parcels_in, name='parcels_in'),

    url(r'^regions/$', views.region_types, name='regions_types'),
    url(r'^regions/(?P<region_type>[\w-]+)/$', views.regions, name='regions'),

    url(r'^reverse_geocode/$', views.reverse_geocode, name='reverse_geocode'),
]