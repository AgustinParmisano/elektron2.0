# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-14 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20171213_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='datetimetask',
            name='repeat_criteria',
            field=models.IntegerField(default=0),
        ),
    ]
