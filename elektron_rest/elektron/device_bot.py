import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import datetime
import json
import ast
import requests

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensors/new_data")
    client.subscribe("server/new_order")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    randata = random.randint(0,101)
    msg = {'device': "1", 'date': datetime.datetime.now(), 'data_value': randata}
    publish.single(msg.topic, msg, hostname="localhost")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(localhost, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
