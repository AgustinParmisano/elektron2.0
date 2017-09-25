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

def on_connect(client, userdata, flags, rc):
   print("Connected with result code "+str(rc))

   # Subscribing in on_connect() means that if we lose the connection and
   # reconnect then subscriptions will be renewed.
   #client.subscribe("sensors/new_sensor")
   client.subscribe("data_to_web")

def on_message(client, userdata, msg):
   #print(msg.topic+" "+str(msg.payload))
   print "Sending data from MQTT(Device) to WebSocket(Web Interface)"
   data_json = ast.literal_eval(msg.payload)
   print data_json

   q.put(data_json)


class MqttClient(object):
    """docstring for MqttClient."""
    def __init__(self, client=mqtt.Client()):
        super(MqttClient, self).__init__()
        self.client = client
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect("localhost", 1883, 60)
        #self.client.connect("158.69.223.78", 1883, 60)

    def get_client(self):
        return self.client

    def set_on_connect(self, func):
        self.on_connect = func

    def publish(self, message, topic):
         print("Sending %s " % (message))
         self.client.publish(str(topic), message)
         return "Sending msg: %s " % (message)

mqtt = MqttClient()
mqtt.client.loop_start()

class Device(object):
    """docstring for Device."""
    def __init__(self, ip, mac, label, devicestate, data_range_min, data_range_max):
        super(Device, self).__init__()
        self.device_ip = ip
        self.device_mac = mac
        self.label = label
        self.devicestate = devicestate
        self.data_range_min = data_range_min
        self.data_range_max = data_range_max
        self.data_value = 0
        if data_range_min > data_range_max:
            print("min > max, setting defaults min: 0; max: 100")
            data_range_max = 0
            data_range_min = 100

        self.data_range = (data_range_min, data_range_max)

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


def device_constructor():
    ip = raw_input("Device ip (f.e: 10.0.0.2): ") or "10.0.0.99"
    mac = raw_input("Device mac (f.e: 12:34:56:78): ") or "99:99:99:99"
    label = raw_input("Device label (f.e: device1): ") or "device99"
    devicestate = raw_input("Device State (f.e: 1): ") or "1"
    value_range_max = input("Device max value (f.e: 100): ") or 100
    value_range_min = input("Device min value (f.e: 0): ") or 0

    if value_range_min > value_range_max:
        print("min > max, setting defaults min: 0; max: 100")
        value_range_max = 0
        value_range_min = 100

    data_range = (value_range_min, value_range_max)

    device = Device(ip, mac, label, devicestate, value_range_min, value_range_max)

    return device

def data_generator(datarange):
    randata = random.randint(datarange[0],datarange[1])
    return randata

time.sleep(1)

def uniq_device_test():
    device = device_constructor()
    drange = device.get_data_range()

    for i in range(0,30):
            time.sleep(5)
            print i
            data = data_generator(drange)
            device.set_data_value(data)
            topic = "sensors/new_data"
            data = str(device)
            print data
            mqtt.publish(data, topic)

def multiple_devices_test():
    ok = True

    lampara_led = Device("192.168.0.50", "00:04:f4:f2:f1:d0", "lampara led", "1",  0, 50)
    pc_server = Device("192.168.0.51", "00:04:f2:f5:7f:57", "pc server", "1",  30, 70)
    printer3d = Device("192.168.0.52", "00:04:8f:0f:1f:b9", "printer3d", "1",  50, 100)
    bc_miner = Device("192.168.0.53", "60:be:fe:45:af:e0", "bc miner", "1",  80, 100)
    devices = [lampara_led, pc_server, printer3d, bc_miner]

    ranges = [devices[0].data_range, devices[1].data_range, devices[2].data_range, devices[3].data_range]

    i = 0

    while ok:
        if i >= 4:
            time.sleep(5)
            i = 0
        time.sleep(1)
        data = data_generator(ranges[i])
        devices[i].set_data_value(data)
        topic = "sensors/new_data"
        print "Sending data %s for device %s ..." % (devices[i].data_value, devices[i].label)
        data = str(devices[i])
        mqtt.publish(data, topic)
        i+=1

opt = input("0 para single device test, 1 para multiple device test: ")
if opt == 0:
    uniq_device_test()
else:
    multiple_devices_test()
