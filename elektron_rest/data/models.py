# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from devices.models import Device

# Create your models here.

class Data(models.Model):
    data_value = models.CharField(max_length=100, blank=True, default='0')
    date = models.DateTimeField(default='0')
    device = models.ForeignKey(Device)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        name = self.data_value
        return name + ","

    def save(self, *args, **kwargs):
        super(Data, self).save(*args, **kwargs)
