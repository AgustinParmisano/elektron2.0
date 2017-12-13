# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
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

class DeviceState(models.Model):
    name = models.CharField(max_length=100, blank=True, default='0')
    description = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(DeviceState, self).save(*args, **kwargs)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Device(models.Model):
    device_ip = models.CharField(max_length=100, blank=True, default='0.0.0.0')
    device_mac = models.CharField(max_length=100, blank=True, default='0')
    created = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=100, blank=True, default='Elektron')
    devicestate = models.ForeignKey(DeviceState)
    owner = models.ForeignKey('auth.User', related_name='devices', on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        super(Device, self).save(*args, **kwargs)

    def serialize(self):
        return {
            'id': self.id,
            'device_ip': self.device_ip,
            'device_mac': self.device_mac,
            'created': to_UTC(self.created),
            'label': self.label,
            'devicestate': self.devicestate.serialize(),
            'enabled': self.enabled
        }
