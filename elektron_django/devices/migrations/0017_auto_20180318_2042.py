# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-18 20:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0016_auto_20180313_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 18, 20, 42, 47, 732840)),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_state_date_off',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 18, 20, 42, 47, 732619)),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_state_date_on',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 18, 20, 42, 47, 732546)),
        ),
    ]