import requests
import ast
import json
from Queue import Queue
import paho.mqtt.client as mqtt
from datetime import datetime

def get_tasks_from_server(server_ip, server_port):
    tasks_q = Queue()
    tasks_get = requests.get("http://" + server_ip + ":" + server_port + "/tasks/readytasks")

    if tasks_get.status_code == 200:
        tasks = json.loads(tasks_get.text)["readytasks"]
        ready_tasks = []
        ready_tasks = ready_tasks + tasks[0]['datatask']
        ready_tasks = ready_tasks + tasks[1]['datetimetask']

        """
        for dt in ready_tasks:
            print dt["label"] + " " + dt["taskstate"]["name"]
            print ""
            if dt["taskstate"]["name"] == "ready":
                ready_tasks.append(dt)
        """
        sorted_ready_tasks = sorted(ready_tasks, key=lambda k: k['created'])

        for srt in sorted_ready_tasks:
            print srt["label"]
            print " "
            tasks_q.put(srt)
        return tasks_q
    else:
        print "Error in Django Server: " + str(tasks_get.status_code)
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
    for i in range(0,len(l)):
        if int(l[i]["data_value"]) > int(d):
            return i
    return -1

def datatask_correct(tdate,tdata,l):
    l = data_date_is_greater(tdate,l)
    if l >= 0:
        data_ok = data_is_greater(tdata,l)
        if data_ok >= 0:
            return l
    return -1

def datetimetask_correct(tdate, task_datetime, device_data_list):
    task_datetime_list_ok = []
    datetimenow = datetime.now()
    task_datetime_list = device_data_list #datetime_correct(datetimenow, device_data_list)
    if task_datetime_list >= 0:
        for i in range(0,len(task_datetime_list)):
            data = task_datetime_list[i]
            td = datetime.strptime(task_datetime, '%Y-%m-%dT%H:%M:%S')
            now = datetime.strptime(str(datetimenow), '%Y-%m-%d %H:%M:%S.%f')
            if td < now:
                task_datetime_list_ok.append(data)
                return task_datetime_list_ok
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

            if "data_value" in dt:
                execute_datatasks(dt,task_date,device_data_list,server_ip, server_port)

            if "datetime" in dt:
                execute_datetimetasks(dt,task_date,device_data_list,server_ip, server_port)


def execute_datatasks(dt,td,dl,server_ip, server_port):
    task_data = dt['data_value']
    task_date = datetime.strptime(td, '%Y-%m-%dT%H:%M:%S.%f')
    data_ok = datatask_correct(task_date, task_data, dl)

    if data_ok >= 0:
        execute_datatask_function(dt, server_ip, server_port)


def execute_datetimetasks(dtt,td,dl,server_ip, server_port):
    task_datetime = dtt['datetime']
    task_date = datetime.strptime(td, '%Y-%m-%dT%H:%M:%S.%f')
    data_ok = datetimetask_correct(task_date, task_datetime, dl)

    if data_ok >= 0:
        execute_datetimetask_function(dtt, server_ip, server_port)


def execute_datatask_function(task, server_ip, server_port):
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

    if update_task_state.status_code == 200:
        print task_function["name"] + " State Update!"
    else:
        print "Some error updating state of task" + task_function["name"]

def execute_datetimetask_function(task, server_ip, server_port):
    print str(task["id"]) + " " + task["label"]
    task_function = task["taskfunction"]
    task_device = task["device"]
    task_state = task["taskstate"]

    if task_function["name"] == "shutdown":
        print task_function["name"] + " " + task_device["label"]
        print "Enviar msg al servidor para apagar el dispostivo"
        task_data = {'taskstate':'2', 'taskfunction': + task_function["id"], 'label': task["label"], 'description': task["description"], 'datetime': task["datetime"], 'device_mac': task_device["device_mac"], 'owner': 'root' }
        device_data = {'device_ip': task_device["device_ip"], 'device_mac': task_device["device_mac"], 'devicestate': task_device["devicestate"]['id'], 'label': task_device["label"], 'owner': 'root'}
        function_exec_res = requests.post("http://" + server_ip + ":" + server_port + "/devices/" + str(task_device["id"]) + "/shutdown", data=device_data)

        if function_exec_res.status_code == 200:
            update_task_state = requests.post("http://" + server_ip + ":" + server_port + "/tasks/datetimetasks/" + str(task["id"]) + "/update", data=task_data)
        else:
            print("Cannot apply function %s to device %s " % (str(task_function["name"]), str(task_device["label"])))

    if task_function["name"] == "turnon":
        print task_function["name"] + " " + task_device["label"]
        print "Enviar msg al servidor para prender el dispostivo"
        task_data = {'taskstate':'2', 'taskfunction': + task_function["id"], 'label': task["label"], 'description': task["description"], 'datetime': task["datetime"], 'device_mac': task_device["device_mac"], 'owner': 'root' }
        device_data = {'device_ip': task_device["device_ip"], 'device_mac': task_device["device_mac"], 'devicestate': task_device["devicestate"]['id'], 'label': task_device["label"], 'owner': 'root'}
        function_exec_res = requests.post("http://" + server_ip + ":" + server_port + "/devices/" + str(task["id"]) + "/turnon", data=device_data)

        if function_exec_res.status_code == 200:
            update_task_state = requests.post("http://" + server_ip + ":" + server_port + "/tasks/datetimetasks/" + str(task["id"]) + "/update", data=task_data)
        else:
            print("Cannot apply function %s to device %s " % (str(task_function["name"]), str(task_device["label"])))

    if update_task_state.status_code == 200:
        print task["label"] + " State Update!"
    else:
        print "Some error updating state of task" + task_function["name"]

#remote_ip = "158.69.223.78"
remote_ip = "localhost"
port = "8000"
print "Starting Task Handler Daemon . . ."
while True:
    tasksq = get_tasks_from_server(remote_ip,port)
    if tasksq:
        execute_tasks(tasksq, remote_ip,port)
    else:
        print "Error in get task from server"
