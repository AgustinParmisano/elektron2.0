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
        #print("MSG decrypted TYPE: {}".format(type(msg_aes256)))
        #print("MSG decrypted STR: {}".format(str(msg_aes256)))
        return msg_aes256
    except Exception as e:
        print("Exception i decrypt_aes256: {}".format(str(e)))
        #raise

def msg_ws(msg):
    resp = publish.single("data_to_web", msg, hostname="localhost")
    return resp


tryed = datetime.datetime.now()
global data_block
data_block = []

def save_data_block(mqtt_data):
    #print "Sending MQTT Data to Server: "
    global tryed
    data_block.append(mqtt_data)
    now = datetime.datetime.now()
    #print("DATA BLOCK LEN: {}".format(len(data_block)))
    #print("TRYED: {}".format(now > tryed))
    if len(data_block) > 1 or (now > tryed):
        tryed = tryed + datetime.timedelta(seconds=30)

        #print("Saving Block Data: {}".format(str(data_block)))
        while len(data_block) > 0:
            data = data_block.pop()
            time.sleep(0.1)

            requests.post("http://localhost:8000/data/create", data=data)
            print("Data Saved!: {}".format(str(data)))


    return True

"""
def check_data(mqtt_data):
    #print "Sending MQTT Data to Server: "
    #print mqtt_data
    #result = requests.post("http://localhost:8000/data/create", data=mqtt_data)

    result = save_data_block(data_block)
    ##print result
    return result
"""

def check_device(device_mqtt):
    device = requests.post("http://localhost:8000/devices/mac", data=device_mqtt)

    if device.status_code == 200:
        #print "Device does exists in system. Checking if its enabled."
        is_enabled = json.loads(device.content)["device"]["enabled"]
        label = json.loads(device.content)["device"]["label"]
        ip = json.loads(device.content)["device"]["device_ip"]
        state = json.loads(device.content)["device"]["devicestate"]["name"]

        #print "Device State"
        #print state
        if device_mqtt['state'] == str(0):
            #print "Device is On"
            device_state = "on"
        if device_mqtt['state'] == str(1):
            #print "Device is Off"
            device_state = "off"

        is_ok = False
        if is_enabled and device_state == "on":
            #print "Device is On and Enabled"
            is_ok = True

        #print "is_enabled"
        #print is_enabled
        if is_ok:
            #print "Device " + json.loads(device.content)["device"]["label"] + " is enabled"
            result = (0,label)
        else:
            result = (1,label)

        #print("Device MQTT state {} device system state {}".format(device_state, state))
        if device_mqtt['ip'] != ip:
            ipchange = requests.post("http://localhost:8000/devices/updateip", data=device_mqtt).status_code
            if ipchange != 200:
                print "Warning!: IP failed to change! "

        if device_state != state:
            ipchange = requests.post("http://localhost:8000/devices/updatestate", data=device_mqtt).status_code
            if ipchange != 200:
                print "Warning!: State failed to change! "

    else:
        result = requests.post("http://localhost:8000/devices/create", data=device_mqtt).status_code
        #print "Device does not exists in system. Creating it."
        if result == 200:
            result = (0,"created")
        else:
            result = (1,"error")

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
        #print("MSG: {}".format(msg))
        if str("data_value") in str(msg):
            print("Warning!: Message {} is raw! Need to encrypt with AES256 for more security!".format(str(msg)))
            pass
        else:
            #print("Warning!: Message {} is encrypted with AES256 ! Decryting message . . .".format(str(msg)))
            msg = decrypt_aes256(msg)
            #print("MSG DECRYPTED: {}".format(str(msg)))

        mqtt_data = ast.literal_eval(str(msg)) #json.loads(str(msg.payload))
        #mqtt_data # = remove_duplicated_msg(mqtt_data)
        #print "--------------mqtt_data--------------"
        #print mqtt_data
        time_sleep = 1
        try:
            device_ok = check_device(mqtt_data)
            if device_ok[0] == 0:
                mqtt_data = ast.literal_eval(json.dumps(mqtt_data))
                #mqtt_data["date"] = datetime.datetime.now()
                mqtt_data["label"] = device_ok[1]
                message = str(mqtt_data)

                #print "--------------message--------------"
                #print message
                msg_ws(message)
                result = save_data_block(mqtt_data)
        except Exception as e:
            print "Server is down, waiting for " + str(time_sleep) + " seconds to reconnect . . ."
            if time_sleep < 5:
                time_sleep += 1
            time.sleep(time_sleep)

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
    while True:
        time_sleep = 0
        try:
            #print "Starting MQTT"
            mqtt = MqttClient()
            #mqtt.client.loop_start()
            mqtt.client.loop_forever()
            time_sleep = 0
        except Exception as e:
            print "Server is down, waiting for " + str(time_sleep) + " seconds to reconnect . . . \n"
            if time_sleep < 5:
                time_sleep += 1
            time.sleep(time_sleep)
            pass
