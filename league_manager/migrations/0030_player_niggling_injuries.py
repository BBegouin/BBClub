# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-06 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_manager', '0029_auto_20161106_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='niggling_injuries',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
