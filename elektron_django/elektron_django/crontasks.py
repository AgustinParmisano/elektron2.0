from datetime import datetime
from datetime import timedelta

class CronTask(object):
    """docstring for CronTask."""
    #def __init__(self, id, name, description, device, repeats, creation, tfunction):
    def __init__(self, **kwargs):
        super(CronTask, self).__init__()
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.description = kwargs["description"]
        self.device = kwargs["device"]
        self.devicedata = []
        self.repeats = kwargs["repeats"]
        self.repetitions_done = kwargs["repetitions_done"]
        self.last_run =  kwargs["last_run"]
        self.state = "1" #ready
        self.creation = kwargs["creation"]
        self.tfunction = kwargs["tfunction"]

class DateTimeTask(CronTask):
    """docstring for DateTimeTask."""
    def __init__(self, kwargs):
        super(DateTimeTask, self).__init__(**kwargs)
        self.datetime = kwargs["datetime"]
        self.task_data = {'id':self.id,'taskstate':self.state, 'repeats':self.repeats, 'last_run':self.last_run, 'datetime':self.datetime}
        self.url = "/tasks/datetimetask/"
        self.repeat_criteria = kwargs["repeat_criteria"]

    def execute(self, taskhandler):
        try:
            self.datetime = self.datetime.split('.')[0]
        except Exception as e:
            print("Exception in executa datetime tas {} : {}".format(self.name, str(e)))
            pass
        self.datetime = datetime.strptime(self.datetime, '%Y-%m-%dT%H:%M:%S')
        if self.repeats > 0 and self.state == "1":
            if self.datetime < datetime.now():
                    print "!!!!!!!Excecuting task!!!!!!!!! " + self.name
                    self.repeats = self.repeats - 1
                    self.repetitions_done = self.repetitions_done + 1
                    taskhandler.execute_task_function(self)
                    #taskhandler.update_task_state(self)

        else:
            self.state = "2" #done
            taskhandler.update_task_state(self)

    def update(self):
        print "Updating " + self.name
        if self.repeat_criteria == 0:
            self.datetime = self.datetime + timedelta(hours=24) #repeats per day
        else:
            self.datetime = self.datetime + timedelta(hours=1) #repeats per hour
        self.task_data = {'id':self.id,'taskstate':self.state, 'repeats':self.repeats, 'last_run':self.last_run, 'datetime':self.datetime}
        print self.datetime

class DataTask(CronTask):
    """docstring for DataTask."""

    def __init__(self, kwargs):
        super(DataTask, self).__init__(**kwargs)
        self.datacomp = kwargs["data"]
        self.comparator = kwargs["comparator"]
        self.task_data = {'id':self.id,'taskstate':self.state, 'repeats':self.repeats, 'last_run':self.last_run}
        self.url = "/tasks/datatask/"

    def execute(self, taskhandler):
        print("DATA TASK:")
        print(self)
        if self.repeats > 0 and self.state == "1":
            if len(self.devicedata) != 0:
                if self.last_run < self.devicedata["date"]:
                    print "Excecuting task " + self.name
                    self.repeats = self.repeats - 1
                    self.repetitions_done = self.repetitions_done + 1
                    if self.comparator > 0:
                        if float(self.devicedata["data_value"]) > float(self.datacomp):
                            taskhandler.execute_task_function(self)
                    if self.comparator < 0:
                        if float(self.devicedata["data_value"]) < float(self.datacomp):
                            taskhandler.execute_task_function(self)
                    if self.comparator == 0:
                        if float(self.devicedata["data_value"]) == float(self.datacomp):
                            taskhandler.execute_task_function(self)
        else:
            self.state = "2" #done
            taskhandler.update_task_state(self)

    def update(self):
        print "Updating " + self.name
        self.last_run = datetime.now()
        self.task_data = {'id':self.id,'taskstate':self.state, 'repeats':self.repeats, 'last_run':self.last_run}
        print "TASK DATA: "
        print(self.task_data)
