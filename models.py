from django.contrib.gis.db import models

from django.utils.text import slugify

'''
Regions:
    * AC Muni
    * AC Council

    * City Hood
    * City Police
    * City Fire
    * City DPW
    * City Ward
    * City Council

    * Census Block Group
    * Census Tracts
'''


class RegionType(models.Model):
    id = models.CharField(max_length=60, primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField()

    def __str__(self):
        return self.id


class AdminRegion(models.Model):
    '''
    Abstract base class for Administrative Regions (e.g. neighborhoods, municipalities, police zones).
    '''
    name = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    type = models.ForeignKey(RegionType, default='', on_delete=models.CASCADE)
    # Geometry
    geom = models.MultiPolygonField(srid=4326)


class Parcel(models.Model):
    objectid = models.BigIntegerField()
    pin = models.CharField(db_index=True, max_length=80)
    mapblocklot = models.CharField(max_length=80)
    shapearea = models.FloatField()
    shapelen = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    addr_number = models.CharField('address number', max_length=20)
    addr_fraction = models.CharField('address fraction', max_length=20)
    addr_street = models.CharField('address street', max_length=40)
    addr_city = models.CharField('address city', max_length=40)
    addr_state = models.CharField('address state', max_length=20)
    addr_unit = models.CharField('address unit', max_length=20)
    addr_zip = models.CharField('address zip', max_length=5)

    def __str__(self):
        return self.pin


class PghHood(AdminRegion):
    objectid = models.BigIntegerField()
    fid_blockg = models.BigIntegerField()
    statefp10 = models.CharField(max_length=80)
    countyfp10 = models.CharField(max_length=80)
    tractce10 = models.CharField(max_length=80)
    blkgrpce10 = models.CharField(max_length=80)
    geoid10 = models.CharField(max_length=80)
    namelsad10 = models.CharField(max_length=80)
    mtfcc10 = models.CharField(max_length=80)
    funcstat10 = models.CharField(max_length=80)
    aland10 = models.BigIntegerField()
    awater10 = models.BigIntegerField()
    intptlat10 = models.CharField(max_length=80)
    intptlon10 = models.CharField(max_length=80)
    shape_leng = models.FloatField()
    fid_neighb = models.BigIntegerField()
    pghdbsdene = models.FloatField()
    perimeter = models.FloatField()
    neighbor_field = models.BigIntegerField()
    neighbor_i = models.BigIntegerField()
    hood = models.CharField(max_length=80)
    hood_no = models.BigIntegerField()
    acres = models.FloatField()
    sqmiles = models.FloatField()
    dpwdiv = models.BigIntegerField()
    unique_id = models.BigIntegerField()
    sectors = models.BigIntegerField()
    shape_le_1 = models.FloatField()
    shape_ar_1 = models.FloatField()
    page_numbe = models.CharField(max_length=80)
    plannerass = models.CharField(max_length=80)
    created_us = models.CharField(max_length=80)
    created_da = models.CharField(max_length=80)
    last_edite = models.CharField(max_length=80)
    last_edi_1 = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Pittsburgh Neighborhood"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        _type = RegionType.objects.get(id='pittsburgh_neighborhood')
        self.type = _type
        self.title = self.hood
        self.name = slugify(self.title).replace('-', '_')
        super(PghHood, self).save(*args, **kwargs)


class PghFireZone(AdminRegion):
    cartodb_id = models.BigIntegerField()
    firezones1 = models.BigIntegerField()
    firezones_field = models.BigIntegerField()
    mapbook = models.CharField(max_length=80)
    olddist_zo = models.CharField(max_length=80)
    dist_zone = models.CharField(max_length=80)
    shape_area = models.FloatField()
    shape_leng = models.FloatField()
    perimeter = models.FloatField()
    area = models.BigIntegerField()
    dist = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Pittsburgh Fire Zone"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        _type = RegionType.objects.get(id='pittsburgh_fire_zone')
        self.type = _type
        self.title = self.dist_zone
        self.name = slugify(self.title).replace('-', '_')
        super(PghFireZone, self).save(*args, **kwargs)


class PghPoliceZone(AdminRegion):
    objectid = models.BigIntegerField()
    perimeter = models.FloatField()
    zone = models.BigIntegerField()

    class Meta:
        verbose_name = "Pittsburgh Police Zone"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        _type = RegionType.objects.get(id='pittsburgh_police_zone')
        self.type = _type
        self.title = str(self.zone)
        self.name = slugify(self.title).replace('-', '_')
        super(PghPoliceZone, self).save(*args, **kwargs)


class PghWard(AdminRegion):
    fid = models.BigIntegerField()
    area = models.FloatField()
    perimeter = models.FloatField()
    wards_field = models.BigIntegerField()
    wards_id = models.BigIntegerField()
    ward = models.BigIntegerField()
    acres = models.FloatField()
    sqmiles = models.FloatField()
    unique_id = models.BigIntegerField()
    council = models.BigIntegerField()
    dpw_insp = models.CharField(max_length=80)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()

    class Meta:
        verbose_name = 'Pittsburgh Ward'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        _type = RegionType.objects.get(id='pittsburgh_ward')
        self.type = _type
        self.title = str(self.ward)
        self.name = slugify(self.title).replace('-', '_')
        super(PghWard, self).save(*args, **kwargs)


class PghCityCouncil(AdminRegion):
    objectid_1 = models.BigIntegerField()
    objectid = models.BigIntegerField()
    intptlat10 = models.CharField(max_length=80)
    intptlon10 = models.CharField(max_length=80)
    shape_leng = models.FloatField()
    council = models.BigIntegerField()
    councilman = models.CharField(max_length=80)
    committee = models.CharField(max_length=80)
    phone = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Pittsburgh City Council District"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        _type = RegionType.objects.get(id='pittsburgh_city_council')
        self.type = _type
        self.title = str(self.council)
        self.name = slugify(self.title).replace('-', '_')
        super(PghCityCouncil, self).save(*args, **kwargs)


class PghPublicWorks(AdminRegion):
    objectid = models.BigIntegerField()
    #pghdbsdedp = models.FloatField()
    perimeter = models.FloatField()
    dpwdivs_field = models.BigIntegerField()
    dpwdivs_id = models.BigIntegerField()
    #sqmiles = models.FloatField()
    #acres = models.FloatField()
    division = models.BigIntegerField()
    #supervsr = models.CharField(max_length=80)
    unique_id = models.BigIntegerField()
    #sq_miles = models.CharField(max_length=80)
    #dpw_divisi = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Pittsburgh DPW Division"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        _type = RegionType.objects.get(id='pittsburgh_dpw_division')
        self.type = _type
        self.title = str(self.division)
        self.name = slugify(self.title).replace('-', '_')
        super(PghPublicWorks, self).save(*args, **kwargs)


class ACMunicipality(AdminRegion):
    objectid = models.IntegerField()
    muni_name = models.CharField(max_length=80)
    muni_type = models.CharField(max_length=80)
    label = models.CharField(max_length=80)
    cog = models.CharField(max_length=80)
    schoold = models.CharField(max_length=80)
    congdist = models.IntegerField()
    fips = models.IntegerField()
    region = models.CharField(max_length=80)
    acres = models.FloatField()
    sqmi = models.FloatField()
    municode = models.CharField(max_length=80)
    cntl_id = models.CharField(max_length=80)
    cntycounci = models.IntegerField()
    eoc = models.CharField(max_length=80)
    assessorte = models.CharField(max_length=80)
    valuationa = models.CharField(max_length=80)
    yearconver = models.IntegerField()
    globalid = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Allegheny County Municipality"
        verbose_name_plural = "Allegheny County Municipalities"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        _type = RegionType.objects.get(id='allegheny_county_municipality')
        self.type = _type
        self.title = self.label
        self.name = slugify(self.title).replace('-', '_')
        super(ACMunicipality, self).save(*args, **kwargs)


class BlockGroup(AdminRegion):
    fid = models.IntegerField()
    affgeoid = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    county = models.CharField(max_length=80)
    tract = models.CharField(max_length=80)
    block_grp = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Census Block Group"
        verbose_name_plural = "Census Block Groups"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        _type = RegionType.objects.get(id='us_block_group')
        self.type = _type
        self.title = self.state + self.county + self.tract + self.block_grp
        self.name = slugify(self.title).replace('-', '_')
        super(BlockGroup, self).save(*args, **kwargs)


class CensusBlock(AdminRegion):
    fid = models.IntegerField()
    state = models.CharField(max_length=80)
    county = models.CharField(max_length=80)
    tract = models.CharField(max_length=80)
    block = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Census Block"
        verbose_name_plural = "Census Blocks"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        _type = RegionType.objects.get(id='us_census_block')
        self.type = _type
        self.title = self.state + self.county + self.tract + self.block
        self.name = slugify(self.title).replace('-', '_')
        super(CensusBlock, self).save(*args, **kwargs)


class SchoolDistrict(AdminRegion):
    object_id = models.IntegerField()
    district_name = models.CharField(max_length=80)

    class Meta:
        verbose_name = "School District"
        verbose_name_plural = "School Districts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        _type = RegionType.objects.get(id='allegheny_county_school_district')
        self.type = _type
        self.title = self.district_name
        self.name = slugify(self.title).replace('-', '_')
        super(SchoolDistrict, self).save(*args, **kwargs)


class CensusTract(AdminRegion):
    geo_id = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    county = models.CharField(max_length=20)
    tract = models.CharField(max_length=20)
    lsad = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Census Tract"
        verbose_name_plural = "Census Tracts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        _type = RegionType.objects.get(id='us_census_tract')
        self.type = _type
        self.title = self.state + self.county + self.tract
        self.name = slugify(self.title).replace('-', '_')
        super(CensusTract, self).save(*args, **kwargs)


class GeocodeSearch(models.Model):
    query_string = models.CharField(max_length=200)
    result_pin = models.CharField(max_length=16)


class BatchGeocodeFile(models.Model):
    file = models.FileField(upload_to="geoservice/")
    address_field = models.CharField(max_length=50)


class AddressPoint(models.Model):
    object_id = models.IntegerField()
    address_id = models.IntegerField()
    street_id = models.IntegerField()
    dup_street_id = models.IntegerField()
    address_type = models.IntegerField()
    full_address = models.CharField(max_length=60)

    address_number = models.CharField(max_length=60)
    address_number_suffix = models.CharField(
        max_length=60)  # letters and fractions

    # directional initial (N, S, E, W)
    street_prefix = models.CharField(max_length=60)
    street_name = models.CharField(max_length=60)
    street_type = models.CharField(max_length=60)

    unit = models.CharField(max_length=60)
    # SUITE, FLR, LOT
    unit_type = models.CharField(max_length=60)
    floor = models.CharField(max_length=60)

    municipality = models.CharField('administrative region', max_length=60)
    city = models.CharField('city used in address', max_length=60)
    county = models.CharField(max_length=60)
    state = models.CharField(max_length=60)

    zip_code = models.CharField(max_length=5)
    zip_code_four = models.CharField(max_length=4)

    comment = models.CharField(max_length=300)
    edit_date = models.CharField(max_length=30)
    source = models.CharField(max_length=60)
    geom = models.PointField()

    address_number_prefix = models.CharField(max_length=60)  # not used
    street_premodifier = models.CharField(max_length=60)  # not used
    street_pretype = models.CharField(max_length=60)  # not used
    street_postmodifier = models.CharField(max_length=60)  # not used
