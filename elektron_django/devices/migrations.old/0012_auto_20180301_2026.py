# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-01 20:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0011_auto_20180301_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 1, 20, 26, 2, 809799)),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_state_date_off',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 1, 20, 26, 2, 809735)),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_state_date_on',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 1, 20, 26, 2, 809709)),
        ),
    ]
