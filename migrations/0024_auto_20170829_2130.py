# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-29 21:30
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoservices', '0023_auto_20170829_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresspoint',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(default=None, srid=4326),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addresspoint',
            name='parent_id',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='addresspoint',
            name='object_id',
            field=models.IntegerField(),
        ),
    ]