# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-19 01:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0018_auto_20180318_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 19, 1, 49, 51, 149208)),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_state_date_off',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 19, 1, 49, 51, 149149)),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_state_date_on',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 19, 1, 49, 51, 149124)),
        ),
    ]
