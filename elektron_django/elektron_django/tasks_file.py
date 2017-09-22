import requests
import ast
import json
from Queue import Queue
import paho.mqtt.client as mqtt

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
    for i in range(0,len(l)):
        if l[i]["date"] > d:
            return i
    return -1

def data_is_greater(d,l):
    for i in range(0,len(l)):
        if l[i]["data_value"] > d:
            return i
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
            data_date_correct = data_date_is_greater(task_date, device_data_list)

            if data_date_correct >= 0:
                task_data = dt['data_value']
                data_value_correct = data_is_greater(task_data, device_data_list)

                if data_value_correct >= 0:
                    print ""
                    print "Dato es mayor a fecha y en valor a la tarea"
                    print "Ejecutar accion y cambiar de estado o ver que hacer"
                    execute_task_function(dt, server_ip, server_port)

def execute_task_function(task, server_ip, server_port):
    print str(task["id"]) + " " + task["label"]
    print task
    task_function = task["taskfunction"]
    task_device = task["device"]
    task_state = task["taskstate"]
    print task_state

    """
    if task_function["name"] == "shutdown":
        print task_function["name"] + " " + task_device["label"]
        print "Enviar msg al servidor para apagar el dispostivo"
        data = {'taskstate':'0', 'taskfunction': + task_function["id"], 'label': task["label"], 'description': task["description"], 'data_value': task["data_value"], 'device_mac': task_device["device_mac"], 'owner': 'root' }
        print data
        update_task_state = requests.post("http://" + server_ip + ":" + server_port + "/tasks/datatasks/" + str(task["id"]) + "/update", data=data)
        #update_task_state.text
        #update_task_state.url
    """
data_tasks_q = get_datatasks_from_server("158.69.223.78","8000")
execute_tasks(data_tasks_q, "158.69.223.78","8000")
