# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-30 23:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0016_auto_20171230_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 30, 23, 36, 17, 20173)),
        ),
    ]
