# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-13 13:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0027_auto_20180313_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 13, 13, 11, 39, 470690)),
        ),
    ]
