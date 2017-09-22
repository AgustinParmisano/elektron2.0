# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class DeviceState(models.Model):
    name = models.CharField(max_length=100, blank=True, default='0')
    description = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(DeviceState, self).save(*args, **kwargs)


class Device(models.Model):
    device_ip = models.CharField(max_length=100, blank=True, default='0.0.0.0')
    device_mac = models.CharField(max_length=100, blank=True, default='0')
    created = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=100, blank=True, default='Elektron')
    devicestate = models.ForeignKey(DeviceState)
    owner = models.ForeignKey('auth.User', related_name='devices', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return self.label


    def save(self, *args, **kwargs):
        super(Device, self).save(*args, **kwargs)
