# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-30 23:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0006_auto_20171230_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 30, 23, 10, 12, 486161)),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_state_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 30, 23, 10, 12, 486085)),
        ),
    ]
