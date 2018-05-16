import requests
import ast
import json
import time
from Queue import Queue
import paho.mqtt.client as mqtt
from datetime import datetime
import sys
from crontasks import DataTask
from crontasks import DateTimeTask

class TaskHandler(object):
    """docstring for TaskHandler."""
    def __init__(self, server_ip, server_port):
        super(TaskHandler, self).__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.session = ""
        self.tasks_q = Queue()

    def run_handler(self):
        try:
            print " "
            print "Running Task Hanlder . . . "
            print " "

            self.authenticate_daemon()

            while True:
                time.sleep(1)
                self.get_tasks_from_server()
                if not self.tasks_q.empty():
                    self.execute_tasks()
                else:
                    print("No Ready Tasks!")
        except Exception as e:
            print("Excpetion in run_handler: {}".format(str(e)))
            time.sleep(5)

    def authenticate_daemon(self):
        print " "
        print "Authenticating Task Hanlder Daemon with Server . . . "
        print " "
        password = str(sys.argv[1])
        user = {'username':'taskd','password':password}
        self.session = requests.Session()
        self.session.post("http://" + self.server_ip + ":" + self.server_port + "/elektronusers/login", data=user)
        return self.session

    def get_tasks_from_server(self):
        print " "
        print "Getting Ready Tasks From Server . . . "
        print " "
        try:
            tasks_get = self.session.get("http://" + self.server_ip + ":" + self.server_port + "/tasks/readytasks")

            if tasks_get.status_code == 200:
                tasks = json.loads(tasks_get.text)["readytasks"]
                ready_datatasks = []
                ready_datetimetasks = []
                ready_datatasks = tasks[0]['datatask'] #Needs refactoring
                ready_datetimetasks = tasks[1]['datetimetask'] #Needs refactoring

                sorted_ready_datatasks = sorted(ready_datatasks, key=lambda k: k['created']) #Needs refactoring
                sorted_ready_datetimetasks = sorted(ready_datetimetasks, key=lambda k: k['created']) #Needs refactoring

                for srdt in sorted_ready_datatasks:
                    print "Proccesing DataTask: " + srdt["label"]
                    print " "
                    datatask = DataTask({"id":srdt["id"], "name":srdt["label"], "description":srdt["description"],"device":srdt["device"],"repeats":srdt["repeats"],"repetitions_done":srdt["repetitions_done"],"creation":srdt["created"],"tfunction":srdt["taskfunction"],"data":srdt["data_value"],"last_run":srdt["last_run"],"comparator":srdt["comparator"]})
                    self.tasks_q.put(datatask)

                for srdtt in sorted_ready_datetimetasks:
                    print "Proccesing DateTimeTask: " + srdtt["label"]
                    print " "
                    datetimetask = DateTimeTask({"id":srdtt["id"], "name":srdtt["label"], "description":srdtt["description"],"device":srdtt["device"],"repeats":srdtt["repeats"],"repetitions_done":srdtt["repetitions_done"],"repeat_criteria":srdtt["repeat_criteria"],"creation":srdtt["created"],"tfunction":srdtt["taskfunction"],"datetime":srdtt["datetime"],"last_run":srdtt["last_run"]})
                    self.tasks_q.put(datetimetask)

                return self.tasks_q

            else:
                print "Error in Get Task From Server: " + str(tasks_get.status_code)
                return False

        except Exception as e:
            print "Exception in Get Task From Server: " + str(e)
            #raise
            return False

    def get_task_device_data(self,task):
        print " "
        print "Getting Task " + task.name + " Device Data . . . "
        print " "
        try:
            task_creation_date = task.creation #passes from date format to /dd/mm/yyyy/hh format
            if task.last_run == "":
                task.last_run = task_creation_date

            tlrs = task.last_run.split("T")[0]

            task_creation_date = ""

            for i in tlrs.split("-"):
                task_creation_date = str(i) + "/" + task_creation_date

            device_data_get = self.session.get("http://" + self.server_ip + ":" + self.server_port + "/devices/"+ str(task.device["id"]) +"/data/"+str(task_creation_date))

            if device_data_get.status_code == 200:
                device_data = json.loads(device_data_get.text)
                if len(device_data["data"]) != 0:
                    device_data_list = device_data["data"][0]#["data_value"]
                    task.devicedata = device_data_list
                else:
                    pass
            else:
                print("Error getting data from server with get_task_device_data:" )
                print(str(device_data_get.status_code))
        except Exception as e:
            print("Exception in get_task_device_data: " + str(e))
            raise

    def execute_tasks(self):
        print " "
        print "Executing Tasks . . . "
        print " "
        while not self.tasks_q.empty():
            item = self.tasks_q.get()
            self.get_task_device_data(item)
            item.execute(self)
            self.tasks_q.task_done()

    def execute_task_function(self,task):
        print " "
        print "Running Task " + task.name + " Functions . . . "
        print " "
        try:
            #print("Executing: " + str(task.id) + " " + str(task.name))

            #print task.tfunction["name"] + " " + task.device["label"]

            #task_data = {'id':task.id,'taskstate':task.state, 'repeats':task.repeats}
            device_data = {'device_ip': task.device["device_ip"], 'device_mac': task.device["device_mac"], 'devicestate': task.device["devicestate"]['id'], 'label': task.device["label"], 'repeats': task.repeats,'repetitions_done':task.repetitions_done, 'owner': 'root'}
            print("Device ID: " + str(task.device["id"]) + " Task Function: " + str(task.tfunction["name"]))
            print("http://" + self.server_ip + ":" + self.server_port + "/devices/" + str(task.device["id"]) + "/"+ task.tfunction["name"])
            function_exec_res = self.session.post("http://" + self.server_ip + ":" + self.server_port + "/devices/" + str(task.device["id"]) + "/"+ task.tfunction["name"], data=device_data)
            time.sleep(1)
            function_exec_res = self.session.post("http://" + self.server_ip + ":" + self.server_port + "/devices/" + str(task.device["id"]) + "/"+ task.tfunction["name"], data=device_data)
            print("Function Execution Response: {}".format(function_exec_res))

            if function_exec_res.status_code == 200:
                self.update_task_state(task)
            else:
                print("Cannot apply function %s to device %s " % (str(task_function["name"]), str(task_device["label"])))
        except Exception as e:
            print("Error in execute_task_function: " + str(e))
            raise

    def update_task_state(self, task):
        task.update()
        update_task_state = self.session.post("http://" + self.server_ip + ":" + self.server_port + task.url + str(task.id) + "/updatestate", data=task.task_data)


#remote_ip = "158.69.223.78"
remote_ip = "localhost"
port = "8000"
print "Starting Task Handler Daemon . . ."

th = TaskHandler(remote_ip, port)

try:
    th.run_handler()
except Exception as e:
    print("Excpetion in run_handler: {}".format(str(e)))
    time.sleep(5)
