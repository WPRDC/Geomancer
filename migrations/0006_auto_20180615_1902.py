# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-06-15 19:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geostuff', '0005_auto_20180515_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pghpublicworks',
            name='acres',
        ),
        migrations.RemoveField(
            model_name='pghpublicworks',
            name='dpw_divisi',
        ),
        migrations.RemoveField(
            model_name='pghpublicworks',
            name='dpwdivs_field',
        ),
        migrations.RemoveField(
            model_name='pghpublicworks',
            name='pghdbsdedp',
        ),
        migrations.RemoveField(
            model_name='pghpublicworks',
            name='sq_miles',
        ),
        migrations.RemoveField(
            model_name='pghpublicworks',
            name='sqmiles',
        ),
        migrations.RemoveField(
            model_name='pghpublicworks',
            name='supervsr',
        ),
        migrations.RemoveField(
            model_name='pghpublicworks',
            name='unique_id',
        ),
    ]
