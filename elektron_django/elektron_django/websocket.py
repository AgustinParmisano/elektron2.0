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
   client.subscribe("sensors/new_data")

def on_message(client, userdata, msg):
   #print(msg.topic+" "+str(msg.payload))
   #print "Sending data from MQTT(Device) to WebSocket(Web Interface)"
   data_json = ast.literal_eval(msg.payload)
   data_json["last_data_time"] = str(datetime.datetime.now())
   q.put(data_json)


class MqttClient(object):
    """docstring for MqttClient."""
    def __init__(self, client=mqtt.Client()):
        super(MqttClient, self).__init__()
        self.client = client
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect("localhost", 1883, 60)

    def get_client(self):
        return self.client

    def set_on_connect(self, func):
        self.on_connect = func

    def publish(message, topic):
         print("Sending %s " % (message))
         publish.single(str(topic), message, hostname="localhost")
         return "Sending msg: %d " % (message)

mqtt = MqttClient()
mqtt.client.loop_start()

#Websockets clients
clients = []

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    tt = datetime.datetime.now()

    def check_origin(self, origin):
        #print "origin: " + origin
        return True

    # the client connected
    def open(self):
        print ("New client connected")
        self.write_message("You are connected")
        clients.append(self)
        tornado.ioloop.IOLoop.instance().add_timeout(timedelta(seconds=1), self.test)

    def test(self):
        try:
            #n = random.randint(0,100)
            #message = {"data": n}
            message = str(q.get())

            message = ast.literal_eval(json.dumps(message))
            message = ast.literal_eval(message)
            #print type(message)
            msg = {}
            msg["device_ip"] = message["device_ip"]
            msg["device_mac"] = message["device_mac"]
            msg["data_value"] = message["data_value"]
            msg["data_datetime"] = message["date"]
            #msg["last_data_time"] = str(datetime.datetime.now())
            message = msg
            #print type(message)
            print "Sending device message to WebInterface"
            print message

            try:
                time.sleep(1)
                self.write_message(message)
            except Exception as e:
                print "Exception in test write message: "
                print e
                raise(e)
        except Exception as e:
            print "Exception in test write message 2: "
            print e
            raise(e)
        else:
            tornado.ioloop.IOLoop.instance().add_timeout(timedelta(seconds=0.1), self.test)

    # the client sent the message
    def on_message(self, message):
        print ("Message: " + message)
        try:
           msg = json.loads(message.payload)
           data_json = {}
           print "MESSAGE FROM WEB SOCKET"
           print "MSG TYPE"
           print type(msg)
           print "MSG DATA"
           print  msg
           #message = ast.literal_eval(message)
           #print("AST Message: " + str(message))

        except Exception as e:
            print ("Exception in on_message:")
            print e
        #self.write_message(message)

    # client disconnected
    def on_close(self):
        print ("Client disconnected")
        clients.remove(self)

socket = tornado.web.Application([(r"/websocket", WebSocketHandler),])

print("Starting WebSocket")
print("Opening port 8888")
socket.listen(8888)

tornado.ioloop.IOLoop.instance().start()
