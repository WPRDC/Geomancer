# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-26 17:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoservices', '0010_auto_20170426_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pghward',
            name='adminregion_ptr',
        ),
        migrations.DeleteModel(
            name='PghWard',
        ),
    ]