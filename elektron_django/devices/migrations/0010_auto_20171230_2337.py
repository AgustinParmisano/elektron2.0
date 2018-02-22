# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-30 23:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0009_auto_20171230_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 30, 23, 37, 56, 394888)),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_state_date_off',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 30, 23, 37, 56, 394822)),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_state_date_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 30, 23, 37, 56, 394796)),
        ),
    ]