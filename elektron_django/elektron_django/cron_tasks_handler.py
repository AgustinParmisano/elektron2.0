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
                ready_datatasks = tasks[0]['datatask']
                ready_datetimetasks = tasks[1]['datetimetask']

                sorted_ready_datatasks = sorted(ready_datatasks, key=lambda k: k['created'])
                sorted_ready_datetimetasks = sorted(ready_datetimetasks, key=lambda k: k['created'])

                for srdt in sorted_ready_datatasks:
                    print "Proccesing DataTask: " + srdt["label"]
                    print " "
                    datatask = DataTask({"id":srdt["id"], "name":srdt["label"], "description":srdt["description"],"device":srdt["device"],"repeats":srdt["repeats"],"creation":srdt["created"],"tfunction":srdt["taskfunction"],"data":srdt["data_value"]})
                    self.tasks_q.put(datatask)

                for srdtt in sorted_ready_datetimetasks:
                    print "Proccesing DateTimeTask: " + srdtt["label"]
                    print " "
                    datetimetask = DateTimeTask({"id":srdtt["id"], "name":srdtt["label"], "description":srdtt["description"],"device":srdtt["device"],"repeats":srdtt["repeats"],"creation":srdtt["created"],"tfunction":srdtt["taskfunction"],"datetime":srdtt["datetime"]})
                    self.tasks_q.put(datetimetask)

                return self.tasks_q

            else:
                print "Error in Get Task From Server: " + str(tasks_get.status_code)
                return False

        except Exception as e:
            print "Exception in Get Task From Server: " + str(e)
            raise
            return False

    def get_task_device_data(self,task):
        print " "
        print "Getting Tasks Device Data . . . "
        print " "
        try:

            print "AAAAAA"
            print task.last_run

            task_creation_date = task.creation #passes from date format to /dd/mm/yyyy/hh format
            tcds = task_creation_date.split("T")[0]
            task_creation_date = ""

            for i in tcds.split("-"):
                task_creation_date = str(i) + "/" + task_creation_date



            device_data_get = self.session.get("http://" + self.server_ip + ":" + self.server_port + "/devices/"+ str(task.device["id"]) +"/data/"+str(task_creation_date))

            if device_data_get.status_code == 200:
                device_data = json.loads(device_data_get.text)
                if len(device_data["data"]) != 0:
                    device_data_list = device_data["data"][0]#["data_value"]
                    print device_data["data"][0]
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
        print "Running Tasks Funtions . . . "
        print " "
        try:
            print("Executing: " + str(task.id) + " " + str(task.name))

            print task.tfunction["name"] + " " + task.device["label"]

            #task_data = {'id':task.id,'taskstate':task.state, 'repeats':task.repeats}
            device_data = {'device_ip': task.device["device_ip"], 'device_mac': task.device["device_mac"], 'devicestate': task.device["devicestate"]['id'], 'label': task.device["label"], 'repeats': task.repeats, 'owner': 'root'}
            function_exec_res = self.session.post("http://" + self.server_ip + ":" + self.server_port + "/devices/" + str(task.device["id"]) + "/"+ task.tfunction["name"], data=device_data)

            if function_exec_res.status_code == 200:
                self.update_task_state(task)
            else:
                print("Cannot apply function %s to device %s " % (str(task_function["name"]), str(task_device["label"])))
        except Exception as e:
            print("Error in execute_task_function: " + str(e))
            raise

    def update_task_state(self, task):
        task_data = {'id':task.id,'taskstate':task.state, 'repeats':task.repeats}
        update_task_state = self.session.post("http://" + self.server_ip + ":" + self.server_port + "/tasks/datatasks/" + str(task.id) + "/updatestate", data=task_data)


#remote_ip = "158.69.223.78"
remote_ip = "localhost"
port = "8000"
print "Starting Task Handler Daemon . . ."

th = TaskHandler(remote_ip, port)
th.run_handler()
