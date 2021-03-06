# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-15 19:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geostuff', '0002_auto_20180515_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='CensusBlock',
            fields=[
                ('adminregion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='geostuff.AdminRegion')),
                ('fid', models.IntegerField()),
                ('state', models.CharField(max_length=80)),
                ('county', models.CharField(max_length=80)),
                ('tract', models.CharField(max_length=80)),
                ('block', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Census Block',
                'verbose_name_plural': 'Census Blocks',
            },
            bases=('geostuff.adminregion',),
        ),
    ]
