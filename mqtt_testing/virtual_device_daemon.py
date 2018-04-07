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
from virtual_device_creator import Device
import time
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


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

class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

key = "1234567890ABCDEF"
key += sys.argv[1] #SSID PASSWORD FOR SALT KEY ENCRYPTION
cipher=AESCipher(key)

def encrypt_aes256(msg):
    try:
        msg_aes256 = cipher.encrypt(msg)
        return msg_aes256
    except Exception as e:
        print("Exception i encrypt_aes256: {}".format(str(e)))
        raise

class MqttClient(object):
    """docstring for MqttClient."""
    def __init__(self, host, client=mqtt.Client()):
        super(MqttClient, self).__init__()
        self.client = client
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(host, 1883, 60)
        #self.client.connect("158.69.223.78", 1883, 60)

    def get_client(self):
        return self.client

    def set_on_connect(self, func):
        self.on_connect = func

    def publish(self, message, topic):
         print("Sending %s " % (message))
         self.client.publish(str(topic), message)
         return "Sending msg: %s " % (message)

class DeviceManager(object):
    """docstring for DeviceManager."""
    def __init__(self, topic, host_ip, devicesq=None):
        super(DeviceManager, self).__init__()
        self.devicesq = []
        self.topic = topic or "sensors/new_data"
        self.host_ip = host_ip or "localhost"
        self.mqtt = MqttClient(host_ip)
        self.mqtt.client.loop_start()
        print self.host_ip

    def add_device(self, device):
        print "add_device"
        self.devicesq.append(device)

    def get_devicesq(self):
        return self.devicesq

    def run_devices(self):
        print "run_devices"
        for device in self.devicesq:
            device = ast.literal_eval(str(device))
            device = Device(device["device_ip"],device["device_mac"],device["label"],device["devicestate"])
            self.run_device(device)

    def run_device(self, device):
        print "run_device"
        randata = device.data_generator()
        device.set_data_value(randata)
        print "\n Sending Device Data via MQTT: "
        print str(device)
        mac_topic = str(device.device_mac)[-5:]
        #self.topic = "sensors/"+ str(mac_topic) + "/new_data"

        device = encrypt_aes256(str(device))

        self.mqtt.publish(str(device),self.topic)
        print "\n"

host_ip = raw_input("Host ip (f.e. localhost): ") or "localhost"
topic = raw_input("Topic (f.e. sensors/new_data): ") or "sensors/new_data"
devicesfile = raw_input("Devices File: ") or "/home/debian/elektron/elektron2.0/mqtt_testing/devices.txt"

dm = DeviceManager(topic, host_ip)

while True:
    time.sleep(5)
    dm.run_devices()
    with open(devicesfile) as df:
        for line in df:
            if line != "":
                if line not in dm.get_devicesq():
                   print "New Device Found!"
                   print line
                   dm.add_device(line)
        df.close()
