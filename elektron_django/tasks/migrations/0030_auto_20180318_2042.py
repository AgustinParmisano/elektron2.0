# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-18 20:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0029_auto_20180318_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 18, 20, 42, 54, 397947)),
        ),
    ]
