from django.contrib.gis import admin
from .models import RegionType, PghCityCouncil, PghPublicWorks, PghPoliceZone,PghHood, PghFireZone, Parcel, ACMunicipality, BlockGroup, AddressPoint

admin.site.register(Parcel, admin.GeoModelAdmin)
admin.site.register(AddressPoint, admin.GeoModelAdmin)
admin.site.register(PghHood, admin.GeoModelAdmin)
#admin.site.register(PghWard, admin.GeoModelAdmin)
admin.site.register(PghCityCouncil, admin.GeoModelAdmin)
admin.site.register(PghPublicWorks, admin.GeoModelAdmin)
admin.site.register(PghPoliceZone, admin.GeoModelAdmin)
admin.site.register(PghFireZone, admin.GeoModelAdmin)
admin.site.register(ACMunicipality, admin.GeoModelAdmin)
admin.site.register(BlockGroup, admin.GeoModelAdmin)
admin.site.register(RegionType, admin.ModelAdmin)