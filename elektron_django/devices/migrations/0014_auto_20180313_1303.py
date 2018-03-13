# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-13 13:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0013_auto_20180313_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='last_run',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 13, 13, 3, 2, 337705)),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_state_date_off',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 13, 13, 3, 2, 337637)),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_state_date_on',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 13, 13, 3, 2, 337609)),
        ),
    ]
