# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import timedelta
from django.conf import settings
from django.utils import timezone

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
    last_state_date_on = models.DateTimeField(default=timezone.now())
    last_state_date_off = models.DateTimeField(default=timezone.now())
    owner = models.ForeignKey('auth.User', related_name='devices', on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)
    last_run = models.DateTimeField(default=timezone.now())
    state_counter_on = models.IntegerField(default=0)
    state_counter_off = models.IntegerField(default=0)
    pluged = models.BooleanField(default=True)

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
            'enabled': self.enabled,
            'last_state_date_on': to_UTC(self.last_state_date_on),
            'last_state_date_off': to_UTC(self.last_state_date_off),
            'state_counter_on': self.state_counter_on,
            'state_counter_off':  self.state_counter_off,
            'pluged':  self.pluged
        }
