import requests
import ast
import json
from Queue import Queue
import paho.mqtt.client as mqtt
from datetime import datetime

datetime_tasks_q = Queue()

def get_datatasks_from_server(server_ip, server_port):
    data_tasks_q = Queue()
    datatasks_get = requests.get("http://" + server_ip + ":" + server_port + "/tasks/datatasks")
    if datatasks_get.status_code == 200:
        datatasks = json.loads(datatasks_get.text)['datatasks']
        ready_datatasks = []
        for dt in datatasks:
            print dt["label"] + " " + dt["taskstate"]["name"]
            print ""
            if dt["taskstate"]["name"] == "ready":
                ready_datatasks.append(dt)

        sorted_ready_datatasks = sorted(ready_datatasks, key=lambda k: k['created'])

        for srdt in sorted_ready_datatasks:
            data_tasks_q.put(srdt)
        return data_tasks_q
    else:
        print "Error in Django Server: " + str(datatasks.status_code)
        return False

def data_date_is_greater(d,l):
    data_date_greater_list = []
    for i in range(0,len(l)):
        data = l[i]
        td = datetime.strptime(data["date"], '%Y-%m-%dT%H:%M:%S.%f')
        if td > d:
            data_date_greater_list.append(data)
            return data_date_greater_list
    return -1

def data_is_greater(d,l):
    print "d: " + str(d)
    print len(l)
    for i in range(0,len(l)):
        if int(l[i]["data_value"]) > int(d):
            print l[i]
            return i
    return -1

def data_correct(td,l):
    d = data_date_is_greater(td,l)
    data_ok = data_is_greater(d,l)
    if data_ok >= 0:
        return l
    else:
        return -1

def execute_tasks(task_queue, server_ip, server_port):
    while not task_queue.empty():
        dt = task_queue.get()
        device = dt["device"]
        task_date = dt['created']
        device_data_get = requests.get("http://" + server_ip + ":" + server_port + "/devices/"+ str(dt["device"]["id"]) +"/data")

        if device_data_get.status_code == 200:
            device_data = json.loads(device_data_get.text)
            device_data_list = device_data["data"]
            task_data = dt['data_value']
            task_date = datetime.strptime(task_date, '%Y-%m-%dT%H:%M:%S.%f')
            data_ok = data_correct(task_date, device_data_list)

            if data_ok >= 0:
                execute_task_function(dt, server_ip, server_port)


def execute_task_function(task, server_ip, server_port):
    print str(task["id"]) + " " + task["label"]
    task_function = task["taskfunction"]
    task_device = task["device"]
    task_state = task["taskstate"]

    if task_function["name"] == "shutdown":
        print task_function["name"] + " " + task_device["label"]
        print "Enviar msg al servidor para apagar el dispostivo"
        task_data = {'taskstate':'2', 'taskfunction': + task_function["id"], 'label': task["label"], 'description': task["description"], 'data_value': task["data_value"], 'device_mac': task_device["device_mac"], 'owner': 'root' }
        device_data = {'device_ip': task_device["device_ip"], 'device_mac': task_device["device_mac"], 'devicestate': task_device["devicestate"]['id'], 'label': task_device["label"], 'owner': 'root'}
        function_exec_res = requests.post("http://" + server_ip + ":" + server_port + "/devices/" + str(task_device["id"]) + "/shutdown", data=device_data)

        if function_exec_res.status_code == 200:
            update_task_state = requests.post("http://" + server_ip + ":" + server_port + "/tasks/datatasks/" + str(task["id"]) + "/update", data=task_data)
        else:
            print("Cannot apply function %s to device %s " % (str(task_function["name"]), str(task_device["label"])))

    if task_function["name"] == "turnon":
        print task_function["name"] + " " + task_device["label"]
        print "Enviar msg al servidor para prender el dispostivo"
        task_data = {'taskstate':'2', 'taskfunction': + task_function["id"], 'label': task["label"], 'description': task["description"], 'data_value': task["data_value"], 'device_mac': task_device["device_mac"], 'owner': 'root' }
        device_data = {'device_ip': task_device["device_ip"], 'device_mac': task_device["device_mac"], 'devicestate': task_device["devicestate"]['id'], 'label': task_device["label"], 'owner': 'root'}
        function_exec_res = requests.post("http://" + server_ip + ":" + server_port + "/devices/" + str(task["id"]) + "/turnon", data=device_data)

        if function_exec_res.status_code == 200:
            update_task_state = requests.post("http://" + server_ip + ":" + server_port + "/tasks/datatasks/" + str(task["id"]) + "/update", data=task_data)
        else:
            print("Cannot apply function %s to device %s " % (str(task_function["name"]), str(task_device["label"])))

    if update_task_state == 200:
        print task_function["name"] + " State Update!"
    else:
        print "Some error updating state of task" + task_function["name"] 

#remote_ip = "158.69.223.78"
remote_ip = "localhost"
port = "8000"

data_tasks_q = get_datatasks_from_server(remote_ip,port)
#datetime_task_q = get_datatasks_from_server(remote_ip,port)
execute_tasks(data_tasks_q, remote_ip,port)
