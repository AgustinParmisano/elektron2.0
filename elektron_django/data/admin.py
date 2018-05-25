# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Data, DataPerHour

# Register your models here.
admin.site.register(Data)
admin.site.register(DataPerHour)
