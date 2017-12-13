# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from devices.models import Device, DeviceState
from datetime import timedelta
from django.conf import settings

# Create your models here.

def to_UTC(date):
    """
    utc = settings.UTC
    if utc < 0:
        date = date - timedelta(hours=abs(utc))
    elif(utc >= 0):
        date = date + timedelta(hours=abs(utc))
    """
    return date

class Data(models.Model):
    data_value = models.CharField(max_length=100, blank=True, default='0')
    date = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(Device)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        name = self.data_value
        return name

    def save(self, *args, **kwargs):
        super(Data, self).save(*args, **kwargs)

    def serialize(self):
        return {
            'id': self.id,
            'data_value': self.data_value,
            'date': to_UTC(self.date),
            'device': self.device.serialize()
        }
