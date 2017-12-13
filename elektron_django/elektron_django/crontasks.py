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

    def execute(self, taskhandler):
        if self.repeats > 0 and self.state == "1":
            """print "--------CronTask Execute-----------"
            print self.devicedata["date"]
            print self.last_run
            print self.devicedata["data_value"]
            print self.datacomp
            print self.comparator
            print "-------- End CronTask Execute-----------"
            """
            if len(self.devicedata) != 0:
                print "self.datetime: " + str(self.datetime)
                print "datetime.now(): " + str(datetime.now())
                self.datetime = datetime.strptime(self.datetime, '%Y-%m-%dT%H:%M:%S')
                if self.datetime < datetime.now():
                        print "Excecuting task " + self.name
                        self.repeats = self.repeats - 1
                        taskhandler.execute_task_function(self)
        else:
            self.state = "2" #done
            taskhandler.update_task_state(self)

    def update(self):
        print "Updating " + self.name
        self.datetime = self.datetime + timedelta(hours=24) #repeats per day
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
        if self.repeats > 0 and self.state == "1":
            """print "--------CronTask Execute-----------"
            print self.devicedata["date"]
            print self.last_run
            print self.devicedata["data_value"]
            print self.datacomp
            print self.comparator
            print "-------- End CronTask Execute-----------"
            """
            if len(self.devicedata) != 0:
                if self.last_run < self.devicedata["date"]:
                    print "Excecuting task " + self.name
                    self.repeats = self.repeats - 1
                    if self.comparator > 0:
                        if self.devicedata["data_value"] > self.datacomp:
                            taskhandler.execute_task_function(self)
                    if self.comparator < 0:
                        if self.devicedata["data_value"] < self.datacomp:
                            taskhandler.execute_task_function(self)
                    if self.comparator == 0:
                        if self.devicedata["data_value"] == self.datacomp:
                            taskhandler.execute_task_function(self)
        else:
            self.state = "2" #done
            taskhandler.update_task_state(self)

    def update(self):
        print "Updating " + self.name
        self.last_run = datetime.now()
        self.task_data = {'id':self.id,'taskstate':self.state, 'repeats':self.repeats, 'last_run':self.last_run}
