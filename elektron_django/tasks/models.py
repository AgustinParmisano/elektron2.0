# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from devices.models import Device
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

# Create your models here.

def to_UTC(date):
    utc = settings.UTC
    if utc < 0:
        date = date - timedelta(hours=abs(utc))
    elif(utc >= 0):
        date = date + timedelta(hours=abs(utc))
    return date

class TaskFunction(models.Model):
    name = models.CharField(max_length=100, blank=True, default='deafult function name')
    description = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(TaskFunction, self).save(*args, **kwargs)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

class TaskState(models.Model):
    name = models.CharField(max_length=100, blank=True, default='default state name')
    description = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(TaskState, self).save(*args, **kwargs)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

#Abstract Task
class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=100, blank=True, default='tarea')
    description = models.CharField(max_length=255, blank=True, default='')
    taskstate = models.ForeignKey(TaskState)
    taskfunction = models.ForeignKey(TaskFunction)
    device = models.ForeignKey(Device)
    owner = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)
    repeats = models.IntegerField(default=1)
    last_run = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)

class DateTimeTask(Task):
    datetime = models.DateTimeField(default=timezone.now)

    def serialize(self):

        aux = "No Runs" if self.last_run == None else to_UTC(self.last_run)
        return {
            'id': self.id,
            'label': self.label,
            'description': self.description,
            'taskstate': self.taskstate.serialize(),
            'taskfunction': self.taskfunction.serialize(),
            'device': self.device.serialize(),
            'datetime': to_UTC(self.datetime),
            'created': to_UTC(self.created),
            'repeats': self.repeats,
            'last_run': aux,
        }

class DataTask(Task):
    data_value = models.CharField(max_length=100, blank=True, default='0')
    comparator = models.IntegerField(default=0)

    def serialize(self):

        aux = "No Runs" if self.last_run == None else to_UTC(self.last_run)
        return {
            'id': self.id,
            'label': self.label,
            'description': self.description,
            'data_value': self.data_value,
            'taskstate': self.taskstate.serialize(),
            'taskfunction': self.taskfunction.serialize(),
            'device': self.device.serialize(),
            'created': to_UTC(self.created),
            'repeats': self.repeats,
            'last_run': aux,
            'comparator': self.comparator,
        }
