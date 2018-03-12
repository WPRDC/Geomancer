from django.contrib.gis.utils import LayerMapping
from geostuff.models import *
import subprocess

from .collection_settings import MODEL_MAPPING, ZIP_MAPPING

SOURCE_DIR = "/var/www/wprdc_tools/geostuff/source_data/"  # TODO: make relative
#SOURCE_DIR = "/home/sds25/projects/wprdc-tools/geoservices/source_data/"  # TODO: make relative


# Define how to map source data files to the models.

def add_address_city(zips=ZIP_MAPPING):
    for address in AddressPoint.objects.all():
        try:
            city = zips[address.zip_code]['NAME']
            address.city = city
            address.save()
        except:
            print('ERROR: {}'.format(address.zip_code))


def run(update_parcel=False, update_addr=False, verbose=True, mapping=MODEL_MAPPING):

    subprocess.run(['psql', 'django', '-c', 'TRUNCATE geostuff_adminregion cascade'])
	
    # if updating parcel, first truncate its table, otherwise remove it from mapping so it's not updated
    if update_parcel:
        subprocess.run(['psql', 'django', '-c', 'TRUNCATE geostuff_parcel'])
    else:
        del (mapping['parcel'])

    # if updating address, first truncate its table, otherwise remove it from mapping so it's not updated
    if update_addr:
        subprocess.run(['psql', 'django', '-c', 'TRUNCATE geostuff_addresspoint'])
    else:
        del (mapping['address'])

    for title, data in mapping.items():
        print(title)
        shp = SOURCE_DIR + data['source']
        mapping = data['mapping']
        model = globals()[data['model']]
        lm = LayerMapping(
            model, shp, mapping,
            transform=True, encoding='iso-8859-1',
        )
        lm.save(strict=False, verbose=verbose)

    if update_addr:
        add_address_city()
