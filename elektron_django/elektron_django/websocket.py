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

q = Queue.Queue() #MQTT message Queue
clients = [] #Websockets clients

def on_connect(client, userdata, flags, rc):
   print("Connected with result code "+str(rc))

   # Subscribing in on_connect() means that if we lose the connection and
   # reconnect then subscriptions will be renewed.
   #client.subscribe("sensors/new_sensor")
   client.subscribe("data_to_web")

def on_message(client, userdata, msg):
    print msg.payload
    #{'device_label': u'Lampara bajo cons', 'data_value': '19.77', 'device_ip': '192.168.0.4', 'label': 'Elektron', 'date': datetime.datetime(2018, 4, 23,18, 20, 23, 655959), 'device_mac': '60:01:94:06:85:45'}
    data_json = ast.literal_eval(msg.payload)
    data_json["last_data_time"] = str(datetime.datetime.now())

    if len(clients) > 0:
       q.put(data_json)
    else:
       #print q
       q.queue.clear()

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
         ##print("Sending %s " % (message))
         publish.single(str(topic), message, hostname="localhost")
         return "Sending msg: %d " % (message)

mqtt = MqttClient()
mqtt.client.loop_start()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    tt = datetime.datetime.now()

    def check_origin(self, origin):
        return True

    # the client connected
    def open(self):
        try:
            print("Client {} is trying to connect. ".format(str(self)))
            if self not in clients:
                print ("New client connected")
                #self.write_message("You are connected")
                clients.append(self)
                print "Clients: " + str(len(clients))
                tornado.ioloop.IOLoop.instance().add_timeout(timedelta(seconds=1), self.ws_msg_loop)
        except Exception as e:
            print("Exception in open: {}".format(str(e)))
            raise

    def ws_msg_loop(self):
        #print("Starting ws_msg_loop!")
        try:
            #n = random.randint(0,100)
            #message = {"data": n}
            if len(clients) > 0:
                message = str(q.get())

                message = ast.literal_eval(json.dumps(message))
                message = ast.literal_eval(message)
                msg = {}
                #print("SENDING WEBSOCKET MESSAGE:")
                #print(message)
                msg["device_ip"] = message["ip"]
                msg["device_mac"] = message["mac"]
                msg["device_state"] = message["state"]
                msg["data_value"] = message["data_value"]
                msg["data_datetime"] = message["last_data_time"]
                msg["device_label"] = message["label"]
                message = msg

                #time.sleep(1)
                for c in clients:
                    try:
                        #print "Sending device message to WebInterface for client: " + str(c)
                        #print message
                        c.write_message(message)
                    except Exception as e:
                        print("Exception in ws_msg_loop trying to write message for client {}: ".format(c))
                        #clients.remove(c)
                        raise
            else:
                pass
        except Exception as e:
            print "Exception in ws_msg_loop : "
            print e
            raise
        else:
            tornado.ioloop.IOLoop.instance().add_timeout(timedelta(seconds=0.1), self.ws_msg_loop)

    # the client sent the message
    def on_message(self, message):
        #print ("Message: " + message)
        try:
           msg = json.loads(message.payload)
           data_json = {}
           print "MESSAGE FROM WEB SOCKET"
           print "MSG TYPE"
           print type(msg)
           print "MSG DATA"
           print  msg

        except Exception as e:
            #print ("Exception in on_message:")
            #print e
            print "MESSAGE FROM WEB SOCKET"
            print "MSG TYPE"
            print type(message)
            print "MSG DATA"
            print  message

        #self.write_message(message)

    # client disconnected
    def on_close(self):
        try:
            if self in clients:
                print ("Client disconnected")
                clients.remove(self)
                print "Clients: " + str(len(clients))
                print clients
            else:
                print("Clients: {}".format(clients))
        except Exception as e:
            print("Exception in on_close: {}".format(str(e)))
            raise

socket = tornado.web.Application([(r"/websocket", WebSocketHandler),])

print("\n")
print("Starting WebSocket")
print("Opening port 8888")
socket.listen(8888)

tornado.ioloop.IOLoop.instance().start()
