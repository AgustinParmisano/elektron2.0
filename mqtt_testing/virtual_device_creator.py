import tornado
import tornado.websocket
from tornado import gen
from datetime import timedelta
import datetime, sys, time
import ast
import json
import random
import datetime
import paho.mqtt.client as mqtt
import time
import requests
import Queue

q = Queue.Queue()

class Device(object):
    """docstring for Device."""
    def __init__(self, device_ip="", device_mac="", label="", devicestate=""):
        super(Device, self).__init__()
        self.device_ip = device_ip
        self.device_mac = device_mac
        self.label = label
        self.devicestate = devicestate
        self.data_range_min = 0
        self.data_range_max = 100
        if self.data_range_min > self.data_range_max:
            print("min > max, setting defaults min: 0; max: 100")
            self.data_range_max = 0
            self.data_range_min = 100

        self.data_range = (self.data_range_min, self.data_range_max)
        self.data_value = 0

    def __str__(self):
        return str({
            'device_ip': self.device_ip,
            'device_mac': self.device_mac,
            'label': self.label,
            'devicestate': self.devicestate,
            'data_value': self.data_value,
        })

    def set_data_value(self, data_value):
        self.data_value = data_value

    def get_data_range(self):
        return self.data_range

    def device_constructor(self):
        ip = raw_input("Device ip (f.e: 10.0.0.2): ") or "10.0.0.99"
        mac = raw_input("Device mac (f.e: 12:34:56:78): ") or "99:99:99:99"
        label = raw_input("Device label (f.e: device1): ") or "device99"
        devicestate = raw_input("Device State (f.e: 1): ") or "1"
        value_range_max = input("Device max value (f.e: 100): ") or 100
        value_range_min = input("Device min value (f.e: 0): ") or 0
        self.device_ip = ip
        self.device_mac = mac
        self.label = label
        self.devicestate = devicestate
        self.data_range_min = value_range_min
        self.data_range_max = value_range_max
        return self

    def data_generator(self):
        randata = random.randint(self.data_range_min,self.data_range_max)
        if randata == 0:
            randata = random.randint(0,100)
        self.set_data_value(randata)
        return self.data_value
"""
opt = 0 #input("1 For New Device, 0 to exit: ")

file = open("devices.txt","a")

while opt != 0:
    device = Device()
    device.device_constructor()
    #q.put(device)
    print "New Device created: "
    print str(device)
    file.write(str(device)+"\n")
    opt = input("1 For New Device, 0 to exit: ")

file.close()
"""
