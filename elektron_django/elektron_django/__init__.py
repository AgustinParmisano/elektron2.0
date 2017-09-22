"""
from mqtt import MqttClient
import os

print(os.getpid())

mqtt = MqttClient()
mqtt.client.loop_start()

"""
