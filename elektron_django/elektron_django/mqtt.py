import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import datetime
import json
import ast
import requests
import Queue
import sys
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


qmsg = Queue.Queue()

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
print key
cipher=AESCipher(key)

def decrypt_aes256(encypted_msg):
    try:
        encypted_msg = encypted_msg.decode("utf-8")
        msg_aes256 = cipher.decrypt(encypted_msg)
        print("MSG decrypted TYPE: {}".format(type(msg_aes256)))
        print("MSG decrypted STR: {}".format(str(msg_aes256)))
        return msg_aes256
    except Exception as e:
        print("Exception i decrypt_aes256: {}".format(str(e)))
        raise

def msg_ws(msg):
    resp = publish.single("data_to_web", msg, hostname="localhost")
    return resp

def check_data(mqtt_data):
    #print "Sending MQTT Data to Server: "
    #print mqtt_data
    result = requests.post("http://localhost:8000/data/create", data=mqtt_data)
    ##print result
    return result

def check_device(device_mqtt):
    device = requests.post("http://localhost:8000/devices/mac", data=device_mqtt)

    if device.status_code == 200:
        #print "Device does exists in system. Checking if its enabled."
        is_enabled = json.loads(device.content)["device"]["enabled"]
        #print "is_enabled"
        #print is_enabled
        if is_enabled:
            #print "Device " + json.loads(device.content)["device"]["label"] + " is enabled"
            result = 0
        else:
            result = 1

        ipchange = requests.post("http://localhost:8000/devices/updateip", data=device_mqtt).status_code
        if ipchange != 200:
            print "Warning!: IP failed to change! "
    else:
        result = requests.post("http://localhost:8000/devices/create", data=device_mqtt).status_code
        #print "Device does not exists in system. Creating it."
        if result == 200:
            result = True
        else:
            result = False

    return result

def on_connect(client, userdata, flags, rc):
   #print("MQTT Connected with result code "+str(rc))

   # Subscribing in on_connect() means that if we lose the connection and
   # reconnect then subscriptions will be renewed.
   #client.subscribe("sensors/new_sensor")
   client.subscribe("sensors/new_data")


data_list = []
def on_message_device(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))

    try:
        msg = str(msg.payload)
        msg = msg.encode('utf-8').strip()
        print("MSG: {}".format(msg))
        msg = decrypt_aes256(msg)
        print("MSG DECRYPTED: {}".format(str(msg)))

        mqtt_data = ast.literal_eval(str(msg)) #json.loads(str(msg.payload))
        #mqtt_data # = remove_duplicated_msg(mqtt_data)

        device_ok = check_device(mqtt_data)

        #print "device_ok"
        #print device_ok

        if device_ok == 0:
            mqtt_data = ast.literal_eval(json.dumps(mqtt_data))
            message = str(mqtt_data)
            msg_ws(message)
            mqtt_data = check_data(mqtt_data)

    except Exception as e:
        print "Exception in on_message_device : " + str(e)
        raise

def on_subscribe(client, userdata,mid, granted_qos):
   print "userdata : " +str(userdata)

def on_publish(mosq, obj, mid):
   print("mid: " + str(mid))

class MqttClient(object):
    """docstring for MqttClient."""
    def __init__(self, client=mqtt.Client()):
        super(MqttClient, self).__init__()
        self.client = client
        self.client.on_connect = on_connect
        self.client.on_message = on_message_device
        self.client.connect("localhost", 1883, 60)
        actions = Queue.Queue()

    def get_actions_queue(self):
        return self.actions

    def get_client(self):
        return self.client

    def set_on_connect(self, func):
        self.on_connect = func

    def publish(message, topic):
         #print("Sending %s " % (message))
         publish.single(str(topic), message, hostname="localhost")
         return "Sending msg: %d " % (message)

if __name__ == "__main__":
    #print "Starting MQTT"
    mqtt = MqttClient()
    #mqtt.client.loop_start()
    mqtt.client.loop_forever()
