# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-29 16:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0040_auto_20180329_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 29, 16, 49, 3, 540067)),
        ),
    ]
