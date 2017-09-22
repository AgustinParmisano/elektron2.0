import requests
import ast
import json
from Queue import Queue

datetime_tasks_q = Queue()

def get_datatasks_from_server(server_ip, server_port):
    data_tasks_q = Queue()
    datatasks_get = requests.get("http://" + server_ip + ":" + server_port + "/tasks/datatasks")
    if datatasks_get.status_code == 200:
        datatasks = json.loads(datatasks_get.text)['datatasks']
        ready_datatasks = []
        for dt in datatasks:
            print dt["label"] + " " + dt["taskstate"]["name"]
            if dt["taskstate"]["name"] == "ready":
                ready_datatasks.append(dt)

        sorted_ready_datatasks = sorted(ready_datatasks, key=lambda k: k['created'])

        for srdt in sorted_ready_datatasks:
            data_tasks_q.put(srdt)
        return data_tasks_q
    else:
        print "Error in Django Server: " + str(datatasks.status_code)
        return False

def execute_tasks(task_queue):
    while not task_queue.empty():
        dt = task_queue.get()
        print dt["label"] + " " + dt["taskstate"]["name"] + " " + dt["created"]
        

data_tasks_q = get_datatasks_from_server("158.69.223.78","8000")
execute_task(data_tasks_q)
