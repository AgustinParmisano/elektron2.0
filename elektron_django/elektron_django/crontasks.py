from datetime import datetime

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
        ct = CronTask(kwargs["id"],kwargs["name"],kwargs["description"],kwargs["device"],kwargs["repeats"],kwargs["creation"],kwargs["tfunction"])
        CronTask.__init__(ct)
        self.datetime = kwargs["datetime"]

    def execute(self, taskhandler):
        if self.repeats > 0:
            if self.datetime < datetime.now():
                taskhandler.execute_task_function(self)
                self.repeats = self.repeats - 1
                self.last_run = datetime.now()
        else:
            self.state = "2" #done

class DataTask(CronTask):
    """docstring for DataTask."""

    def __init__(self, kwargs):
        #super(DataTask, self).__init__()
        super(DataTask, self).__init__(**kwargs)
        #ct = CronTask(kwargs["id"],kwargs["name"],kwargs["description"],kwargs["device"],kwargs["repeats"],kwargs["creation"],kwargs["tfunction"])
        #CronTask.__init__(ct,kwargs["id"],kwargs["name"],kwargs["description"],kwargs["device"],kwargs["repeats"],kwargs["creation"],kwargs["tfunction"])
        self.datacomp = kwargs["data"]

    def execute(self, taskhandler):
        if self.repeats > 0 and self.state == "1":
            print "--------CronTask Execute-----------"
            print self.devicedata["date"]
            print "LA NO POSTA"
            print self.last_run
            print datetime.now()
            print self.devicedata["data_value"]
            print self.datacomp
            print "-------- End CronTask Execute-----------"

            if len(self.devicedata) != 0:
                if self.last_run < self.devicedata["date"]:
                    if self.devicedata["data_value"] > self.datacomp:
                        print "Excecuting task " + self.name
                        self.repeats = self.repeats - 1
                        print "LA POSTA"
                        print self.last_run
                        taskhandler.execute_task_function(self)
        else:
            print self.state
            self.state = "2" #done
            taskhandler.update_task_state(self)
