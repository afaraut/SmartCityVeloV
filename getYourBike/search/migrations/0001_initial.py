# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stationNum', models.IntegerField()),
                ('stationName', models.CharField(max_length=255)),
                ('stationRegion', models.CharField(max_length=255)),
                ('stationLong', models.FloatField()),
                ('stationLat', models.FloatField()),
            ],
        ),
    ]
