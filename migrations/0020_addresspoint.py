# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-29 20:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoservices', '0019_batchgeocodefile_geocodesearch'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objectid', models.CharField(max_length=60)),
                ('address_id', models.IntegerField()),
                ('street_id', models.IntegerField()),
                ('dup_street_id', models.IntegerField()),
                ('address_type', models.IntegerField()),
                ('full_address', models.CharField(max_length=60)),
                ('address_number_prefix', models.CharField(max_length=60)),
                ('address_number', models.CharField(max_length=60)),
                ('address_number_suffix', models.CharField(max_length=60)),
                ('street_premodifier', models.CharField(max_length=60)),
                ('street_prefix', models.CharField(max_length=60)),
                ('street_pretype', models.CharField(max_length=60)),
                ('street_name', models.CharField(max_length=60)),
                ('street_type', models.CharField(max_length=60)),
                ('street_postmodifier', models.CharField(max_length=60)),
                ('unit', models.CharField(max_length=60)),
                ('unit_type', models.CharField(max_length=60)),
                ('floor', models.CharField(max_length=60)),
                ('municipality', models.CharField(max_length=60)),
                ('county', models.CharField(max_length=60)),
                ('state', models.CharField(max_length=60)),
                ('zip_code', models.CharField(max_length=5)),
                ('zip_code_four', models.CharField(max_length=4)),
                ('comment', models.CharField(max_length=200)),
                ('edit_date', models.DateTimeField()),
                ('source', models.CharField(max_length=60)),
                ('source_id', models.IntegerField()),
            ],
        ),
    ]