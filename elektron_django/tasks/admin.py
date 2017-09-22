# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Task, DateTimeTask, DataTask, TaskState, TaskFunction

# Register your models here.
admin.site.register(DateTimeTask)
admin.site.register(DataTask)
admin.site.register(TaskState)
admin.site.register(TaskFunction)
