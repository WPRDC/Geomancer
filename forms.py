from django import forms

from django.forms import ModelForm
from .models import BatchGeocodeFile

class GeoserviceFileForm(ModelForm):
    class Meta:
        model = BatchGeocodeFile
        fields = ['file', 'address_field']