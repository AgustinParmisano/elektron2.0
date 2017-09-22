#!/bin/bash
$(mosquitto_pub -t sensors/new_data -f ./mqtt_data4)
