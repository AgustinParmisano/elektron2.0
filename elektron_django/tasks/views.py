# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import datetime
from datetime import timedelta
from .models import Task, DateTimeTask, DataTask, TaskState, TaskFunction
from devices.models import Device
from elektronusers.models import User as ElektronUser
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

def to_localtime(date):
    utc = settings.UTC
    """
    if utc < 0:
        date = date + timedelta(hours=abs(utc))
    elif(utc >= 0):
        date = date - timedelta(hours=abs(utc))
    """
    date = date - timedelta(hours=abs(utc))
    return date

def check_device_mac(**kwargs):
    if not 'device_mac' in kwargs:
        return False
    else:
        if type(kwargs['device_mac']) is list:
            kwargs['device_mac'] = kwargs['device_mac'][0]

    return kwargs

def check_task(**kwargs):
    print kwargs
    if not 'taskfunction' in kwargs:
        return False
    else:
        if type(kwargs['taskfunction']) is list:
            kwargs['taskfunction'] = kwargs['taskfunction'][0]

    if not 'label' in kwargs:
        return False
    else:
        if type(kwargs['label']) is list:
            kwargs['label'] = kwargs['label'][0]

    if not 'data_value' in kwargs and not 'datetime' in kwargs:
        return False
    else:
        if 'data_value' in kwargs and type(kwargs['data_value']) is list:
            kwargs['data_value'] = kwargs['data_value'][0]

            if not 'comparator' in kwargs:
                return False
            else:
                if type(kwargs['comparator']) is list:
                    kwargs['comparator'] = kwargs['comparator'][0]

        elif 'datetime' in kwargs and type(kwargs['datetime']) is list:
            kwargs['datetime'] = kwargs['datetime'][0]
            try:
                kwargs['datetime'] = datetime.datetime.strptime(kwargs['datetime'], "%a, %d %b %Y %H:%M:%S %Z")
            except Exception as e:
                pass
            if not 'set_datetime' in kwargs:
                kwargs['set_datetime'] = kwargs['datetime']
            else:
                if type(kwargs['set_datetime']) is list:
                    kwargs['set_datetime'] = kwargs['set_datetime'][0]

            if not 'repeat_criteria' in kwargs:
                return False
            else:
                if type(kwargs['repeat_criteria']) is list:
                    kwargs['repeat_criteria'] = kwargs['repeat_criteria'][0]

    if not 'repeats' in kwargs:
        return False
    else:
        if type(kwargs['repeats']) is list:
            kwargs['repeats'] = kwargs['repeats'][0]

    if not 'set_repeats' in kwargs:
        kwargs['set_repeats'] = kwargs['repeats']
    else:
        if type(kwargs['set_repeats']) is list:
            kwargs['set_repeats'] = kwargs['set_repeats'][0]

    if not 'repetitions_done' in kwargs:
        return False
    else:
        if type(kwargs['repetitions_done']) is list:
            kwargs['repetitions_done'] = kwargs['repetitions_done'][0]

    if not 'last_run' in kwargs:
        kwargs['last_run'] = datetime.datetime.now()
    else:
        if type(kwargs['last_run']) is list:
            kwargs['last_run'] = kwargs['last_run'][0]

    if not 'description' in kwargs:
        return False
    else:
        if type(kwargs['description']) is list:
            kwargs['description'] = kwargs['description'][0]

    if not 'description' in kwargs:
        return False
    else:
        if type(kwargs['description']) is list:
            kwargs['description'] = kwargs['description'][0]


    if not 'taskstate' in kwargs:
        return False
    else:
        if type(kwargs['taskstate']) is list:
            kwargs['taskstate'] = kwargs['taskstate'][0]

    if not 'taskfunction' in kwargs:
        return False
    else:
        if type(kwargs['taskfunction']) is list:
            kwargs['taskfunction'] = kwargs['taskfunction'][0]

    if not 'owner' in kwargs:
        return False
    else:
        if type(kwargs['owner']) is list:
            kwargs['owner'] = kwargs['owner'][0]

    try:
        kwargs['taskstate'] = TaskState.objects.get(id=kwargs['taskstate'])
    except Exception as e:
        #TODO: create default taskstates in settings.py
        kwargs['taskstate'] = TaskState.objects.get(name="ready")

    try:
        kwargs['taskfunction'] = TaskFunction.objects.get(id=kwargs['taskfunction'])
    except Exception as e:
        #TODO: create default taskfunctions in settings.py
        kwargs['taskfunction'] = TaskFunction.objects.get(name="shutdown")

    try:
        kwargs['owner'] = User.objects.get(username=kwargs['owner'])
    except Exception as e:
        #TODO: create default user in settings.py
        kwargs['owner'] = User.objects.get(username="root")

    return kwargs

class IndexView(generic.ListView):
    model = Task

    def get(self, request, *args, **kwargs):
        """Return all tasks."""
        return JsonResponse({'tasks': list(map(lambda x: x.serialize(), Task.objects.all()))})

class DateTimeTaskIndexView(IndexView):
    model = DateTimeTask

    def get(self, request, *args, **kwargs):
        """Return all date time tasks."""
        return JsonResponse({'datetimetasks': list(map(lambda x: x.serialize(), DateTimeTask.objects.all()))})

class DataTaskIndexView(IndexView):
    model = DataTask

    def get(self, request, *args, **kwargs):
        """Return all data tasks."""
        return JsonResponse({'datatasks': list(map(lambda x: x.serialize(), DataTask.objects.all()))})

class DataTaskDetailView(generic.DetailView):
    model = DataTask

    def get(self, request, *args, **kwargs):
        """Return the selected by id DataTask."""
        try:
            return JsonResponse({'datatasks': DataTask.objects.get(id=kwargs["pk"]).serialize()})
        except Exception as e:
            print "Some error ocurred getting Single DataTask with id: " + str(kwargs["pk"])
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DateTimeTaskDetailView(generic.DetailView):
    model = DateTimeTask

    def get(self, request, *args, **kwargs):
        """Return the selected by id DateTimeTask."""
        try:
            return JsonResponse({'datetimetasks': DateTimeTask.objects.get(id=kwargs["pk"]).serialize()})
        except Exception as e:
            print "Some error ocurred getting Single DateTimeTask with id: " + str(kwargs["pk"])
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DatetimeTaskDeviceView(generic.ListView):

    def get(self, request, *args, **kwargs):

        result = Device.objects.get(id=kwargs["pk"])
        device_id = result.serialize()["id"]

        if device_id:
            try:
                tasks = DateTimeTask.objects.all().filter(device=device_id)

            except Exception as e:
                print  "Device you ask does not exist"
                print "Exception: " + str(e)
                raise
                return HttpResponse(status=500)

            if tasks:
                try:

                    task_list = list(tasks)
                    task_list = ({'task': list(map(lambda x: x.serialize(), tasks))})

                    return JsonResponse({'device_tasks': task_list})

                except Exception as e:
                    print "Some error ocurred getting Task Device"
                    print "Exception: " + str(e)
                    return HttpResponse(status=500)

    def post(self, request, *args, **kwargs):

        result = Device.objects.get(id=kwargs["pk"])
        device_id = result.serialize()["id"]

        if device_id:
            try:
                tasks = DateTimeTask.objects.all()

            except Exception as e:
                print  "Device you ask does not exist"
                print "Exception: " + str(e)
                raise
                return HttpResponse(status=500)

            if tasks:
                try:

                    task_list = list(tasks)
                    task_list = ({'task': list(map(lambda x: x.serialize(), tasks))})

                    return JsonResponse({'device_tasks': task_list})

                except Exception as e:
                    print "Some error ocurred getting Task Device"
                    print "Exception: " + str(e)
                    return HttpResponse(status=500)


    def post(self, request, *args, **kwargs):

        result = check_device_mac(**request.POST)

        if result:
            device = Device.objects.get(device_mac=result["device_mac"])

            task = check_task(**request.POST)

            if task:
                try:
                    datatask = DataTask(pk=kwargs['pk'])
                    datatask.description = task["description"]
                    datatask.label = task["label"]
                    datatask.data_value = task["data_value"]
                    datatask.taskstate = task["taskstate"]
                    datatask.taskfunction = task["taskfunction"]
                    datatask.owner = task["owner"]
                    datatask.device = device
                    datatask.created = datetime.datetime.now()

                except Task.DoesNotExist:
                    datatask = DataTask(**task)

                datatask.save()

            return JsonResponse({'status':True})


class DataTaskDeviceView(generic.ListView):

    def get(self, request, *args, **kwargs):

        result = Device.objects.get(id=kwargs["pk"])
        device_id = result.serialize()["id"]

        if device_id:
            try:
                tasks = DateTimeTask.objects.all().filter(device=device_id)

            except Exception as e:
                print  "Device you ask does not exist"
                print "Exception: " + str(e)
                raise
                return HttpResponse(status=500)

            if tasks:
                try:

                    task_list = list(tasks)
                    task_list = ({'task': list(map(lambda x: x.serialize(), tasks))})

                    return JsonResponse({'device_tasks': task_list})

                except Exception as e:
                    print "Some error ocurred getting Task Device"
                    print "Exception: " + str(e)
                    return HttpResponse(status=500)

    def post(self, request, *args, **kwargs):

        result = Device.objects.get(id=kwargs["pk"])
        device_id = result.serialize()["id"]

        if device_id:
            try:
                tasks = DataTask.objects.all()

            except Exception as e:
                print  "Device you ask does not exist"
                print "Exception: " + str(e)
                raise
                return HttpResponse(status=500)

            if tasks:
                try:

                    task_list = list(tasks)
                    task_list = ({'task': list(map(lambda x: x.serialize(), tasks))})

                    return JsonResponse({'device_tasks': task_list})

                except Exception as e:
                    print "Some error ocurred getting Task Device"
                    print "Exception: " + str(e)
                    return HttpResponse(status=500)


class DataTaskCreateView(generic.View):

        #@method_decorator(login_required)
        def post(self, request, *args, **kwargs):
            try:

                result = check_device_mac(**request.POST)
                print result

                if result:
                    device = Device.objects.get(device_mac=result["device_mac"])
                    task = request.POST#check_task(**request.POST)
                    taskstate = TaskState.objects.get(pk=task["taskstate"])
                    print("TASKSTATE")
                    print taskstate
                    taskfunction = TaskFunction.objects.get(name=request.POST["taskfunction"])
                    print("TASKFUNCTION")
                    print taskfunction
                    print request.POST["taskfunction"]
                    owner = User.objects.get(username=task["owner"]) #User editions of tasks need to be revised

                    task = request.POST#check_task(**request.POST)

                    if task:
                        try:
                            datatask = DataTask()
                            datatask.description = task["description"]
                            datatask.label = task["label"]
                            datatask.data_value = task["data_value"]
                            datatask.taskstate = taskstate
                            datatask.taskfunction = taskfunction
                            datatask.owner = owner
                            datatask.device = device
                            datatask.comparator = task["comparator"]
                            datatask.repeats = task["repeats"]
                            datatask.set_repeats = task["repeats"]

                            repetitions_done = lambda x, y: x - y
                            result = repetitions_done(int(datatask.set_repeats), int(datatask.repeats))

                            datatask.repetitions_done = result if result >= 0 else 0
                            #datatask.last_run = task["last_run"]

                        except DataTask.DoesNotExist:
                            datatask = DataTask(**task)

                        print("SAVE????????????")
                        print(datatask.save())

                    return JsonResponse({'status':True})

            except Exception as e:
                    print "Some error ocurred Creating DataTask"
                    print "Exception: " + str(e)
                    return HttpResponse(status=500)


class DataTaskUpdateView(generic.View):

    #@method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            result = check_device_mac(**request.POST)

            if result:
                device = Device.objects.get(device_mac=result["device_mac"])
                task = request.POST#check_task(**request.POST)
                taskstate = TaskState.objects.get(pk=task["taskstate"])
                print("TASKSTATE")
                print taskstate
                taskfunction = TaskFunction.objects.get(name=task["taskfunction"])
                owner = User.objects.get(username=task["owner"]) #User editions of tasks need to be revised

                if task:
                    try:
                        datatask = DataTask.objects.all().filter(pk=kwargs['pk'])
                        datatask = datatask[0]
                        datatask.description = task["description"]
                        datatask.label = task["label"]
                        datatask.data_value = task["data_value"]
                        datatask.taskstate = taskstate
                        datatask.repeats = task["repeats"]
                        datatask.set_repeats = task["repeats"]

                        repetitions_done = lambda x, y: x - y
                        result = repetitions_done(int(datatask.set_repeats), int(datatask.repeats))

                        datatask.repetitions_done = result if result >= 0 else 0
                        datatask.taskfunction = taskfunction
                        datatask.owner = owner
                        datatask.device = device
                        datatask.owner = owner
                        datatask.comparator = task["comparator"]
                        #datatask.last_run = task["last_run"]
                    except Task.DoesNotExist:
                        datatask = DataTask(**task)

                    datatask.save()

                return JsonResponse({'status':True})
        except Exception as e:
                print "Some error ocurred Updating DataTask"
                print "Exception: " + str(e)
                raise
                return HttpResponse(status=500)

class DateTimeTaskCreateView(generic.View):

    #@method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            result = check_device_mac(**request.POST)

            if result:
                device = Device.objects.get(device_mac=result["device_mac"])
                task = request.POST#check_task(**request.POST)
                print "+++++++++TASK+++++++++"
                print task

                taskfunction = TaskFunction.objects.get(name=task["taskfunction"])
                owner = User.objects.get(username=task["owner"]) #User editions of tasks need to be revised
                print("+++++++++DATETIME++++++++")
                print(str(task["datetime"]))
                taskstate = TaskState.objects.get(pk=task["taskstate"])
                task_datetime = datetime.datetime.strptime(task['datetime'], "%a, %d %b %Y %H:%M:%S %Z")
                print("+++++++++DATETIME CONVERTED++++++++")
                print(str(task_datetime))
                task_datetime = to_localtime(task_datetime)
                print("+++++++++DATETIME LOCALTIMED++++++++")
                print(str(task_datetime))

                if task:
                    try:
                        datetimetask = DateTimeTask()
                        datetimetask.description = task["description"]
                        datetimetask.label = task["label"]
                        datetimetask.taskstate = taskstate
                        datetimetask.taskfunction = taskfunction
                        datetimetask.datetime = task_datetime
                        datetimetask.set_datetime = task_datetime
                        datetimetask.repeats = task["repeats"]
                        datetimetask.set_repeats = task["repeats"]

                        repetitions_done = lambda x, y: x - y
                        result = repetitions_done(int(datetimetask.set_repeats), int(datetimetask.repeats))

                        datetimetask.repetitions_done = result if result >= 0 else 0
                        datetimetask.repeat_criteria = task["repeat_criteria"]
                        datetimetask.owner = owner
                        datetimetask.device = device

                    except DateTimeTask.DoesNotExist:
                        datetimetask = DateTimeTask(**task)

                    datetimetask.save()

                return JsonResponse({'status':True})
        except Exception as e:
                print "Some error ocurred Creating DateTimeTask"
                print "Exception: " + str(e)
                return HttpResponse(status=500)
                raise

class DateTimeTaskRemoveView(generic.View):

    #@method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        task = kwargs["pk"]

        if task:
            try:
                datetimetask = DateTimeTask.objects.get(pk=task)
            except DateTimeTask.DoesNotExist:
                return HttpResponse(status=500)

            datetimetask.delete()

        return JsonResponse({'status':True})

class DataTaskRemoveView(generic.View):

    #@method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        task = kwargs["pk"]

        if task:
            try:
                datatask = DataTask.objects.get(pk=task)
            except DataTask.DoesNotExist:
                return HttpResponse(status=500)

            datatask.delete()

        return JsonResponse({'status':True})


class DateTimeTaskUpdateView(generic.View):

    #@method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:

            result = check_device_mac(**request.POST)
            print("POST: ")
            print(request.POST)
            if result:
                device = Device.objects.get(device_mac=result["device_mac"])
                task = request.POST#check_task(**request.POST)
                taskfunction = TaskFunction.objects.get(name=task["taskfunction"])
                owner = User.objects.get(username=task["owner"]) #User editions of tasks need to be revised
                print("+++++++++DATETIME++++++++")
                print(str(task["datetime"]))
                taskstate = TaskState.objects.get(pk=task["taskstate"])
                task_datetime = datetime.datetime.strptime(task['datetime'], "%a, %d %b %Y %H:%M:%S %Z")
                print("+++++++++DATETIME CONVERTED++++++++")
                print(str(task_datetime))
                task_datetime = to_localtime(task_datetime)
                print("+++++++++DATETIME LOCALTIMED++++++++")
                print(str(task_datetime))

                if task:
                    try:
                        datetimetask = DateTimeTask.objects.all().filter(pk=kwargs['pk'])
                        datetimetask = datetimetask[0]
                        datetimetask.description = task["description"]
                        datetimetask.label = task["label"]
                        datetimetask.taskstate = taskstate
                        datetimetask.taskfunction = taskfunction
                        datetimetask.datetime = task_datetime
                        datetimetask.set_datetime = task_datetime
                        datetimetask.repeats = task["repeats"]
                        datetimetask.set_repeats = task["repeats"]

                        repetitions_done = lambda x, y: x - y
                        result = repetitions_done(int(datetimetask.set_repeats), int(datetimetask.repeats))

                        datetimetask.repetitions_done = result if result >= 0 else 0
                        #datetimetask.last_run = datetime.datetime.now()
                        datetimetask.owner = owner
                        datetimetask.repeat_criteria = task["repeat_criteria"]
                        datetimetask.device = device

                    except DateTimeTask.DoesNotExist:
                        datetimetask = DateTimeTask(**task)

                    datetimetask.save()

                return JsonResponse({'status':True})
        except Exception as e:
                print "Some error ocurred Updating DateTimeTask"
                print "Exception: " + str(e)
                return HttpResponse(status=500)
                raise


class ReadyTasksView(generic.View):

    def get(self, request, *args, **kwargs):

        try:

            task_list = []
            datetimetasks = DateTimeTask.objects.all().filter(taskstate=1)
            datatasks = DataTask.objects.all().filter(taskstate=1)
            datatask_list = ({'datatask': list(map(lambda x: x.serialize(), datatasks))})
            datetimetask_list = ({'datetimetask': list(map(lambda x: x.serialize(), datetimetasks))})
            task_list.append(datatask_list)
            task_list.append(datetimetask_list)

            return JsonResponse({'readytasks': task_list})

        except Exception as e:
            print "Error en ReadyTasksView: " + str(e)
            return HttpResponse(status=500)

class ReadyDateTimeTasksView(generic.View):

    def get(self, request, *args, **kwargs):

        try:

            task_list = []
            datetimetasks = DateTimeTask.objects.all().filter(taskstate=1)
            datetimetask_list = ({'datetimetask': list(map(lambda x: x.serialize(), datetimetasks))})
            task_list = datetimetask_list
            return JsonResponse({'readydatetimetasks': task_list})

        except Exception as e:
            print "Error en ReadyDateTimeTasksView: " + str(e)
            return HttpResponse(status=500)

class ReadyDataTasksView(generic.View):

    def get(self, request, *args, **kwargs):

        try:

            task_list = []
            datatasks = DataTask.objects.all().filter(taskstate=1)
            datatask_list = ({'datatask': list(map(lambda x: x.serialize(), datatasks))})
            task_list = datatask_list

            return JsonResponse({'readydatatasks': task_list})

        except Exception as e:
            print "Error en ReadyDataTasksView: " + str(e)

            return HttpResponse(status=500)


class DoneDateTimeTasksView(generic.View):

    def get(self, request, *args, **kwargs):

        try:

            task_list = []
            datetimetasks = DateTimeTask.objects.all().filter(taskstate=2)
            datetimetask_list = ({'datetimetask': list(map(lambda x: x.serialize(), datetimetasks))})
            task_list = datetimetask_list

            return JsonResponse({'donedatetimetasks': task_list})

        except Exception as e:
            print "Error en DoneDateTimeTasksView: " + str(e)
            return HttpResponse(status=500)

class DoneDataTasksView(generic.View):

    def get(self, request, *args, **kwargs):

        try:

            task_list = []
            datatasks = DataTask.objects.all().filter(taskstate=2)
            datatask_list = ({'datatask': list(map(lambda x: x.serialize(), datatasks))})
            task_list = datatask_list

            return JsonResponse({'donedatatasks': task_list})

        except Exception as e:
            print "Error en DoneDataTasksView: " + str(e)
            return HttpResponse(status=500)


class DoneTasksView(generic.View):

    def get(self, request, *args, **kwargs):

        try:

            task_list = []
            datetimetasks = DateTimeTask.objects.all().filter(taskstate=2)
            datatasks = DataTask.objects.all().filter(taskstate=2)
            datatask_list = ({'datatask': list(map(lambda x: x.serialize(), datatasks))})
            datetimetask_list = ({'datetimetask': list(map(lambda x: x.serialize(), datetimetasks))})
            task_list.append(datatask_list)
            task_list.append(datetimetask_list)

            return JsonResponse({'readytasks': task_list})

        except Exception as e:
            print "Error en DoneTasksView: " + str(e)
            return HttpResponse(status=500)

class TaskStatesView(generic.ListView):

    def get(self, request, *args, **kwargs):

        try:
            taskstates = TaskState.objects.all()

        except Exception as e:
            print "Exception: " + str(e)
            raise
            return HttpResponse(status=500)

        if taskstates:
            try:

                taskstate_list = list(taskstates)
                taskstate_list = ({'taskstate': list(map(lambda x: x.serialize(), taskstates))})

                return JsonResponse({'taskstates': taskstate_list})

            except Exception as e:
                print "Some error ocurred getting TaskStates"
                print "Exception: " + str(e)
                return HttpResponse(status=500)

class TaskFunctionsView(generic.ListView):

    def get(self, request, *args, **kwargs):

        try:
            taskfunctions = TaskFunction.objects.all()

        except Exception as e:
            print "Exception: " + str(e)
            raise
            return HttpResponse(status=500)

        if taskfunctions:
            try:

                taskfunctions_list = list(taskfunctions)
                taskfunctions_list = ({'taskfunctions': list(map(lambda x: x.serialize(), taskfunctions))})

                return JsonResponse({'taskfunctions': taskfunctions_list})

            except Exception as e:
                print "Some error ocurred getting TaskStates"
                print "Exception: " + str(e)
                return HttpResponse(status=500)


class DateTimeTaskUpdateStateView(generic.View):

    #@method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        task = request.POST

        if task:
            try:
                datetimetask = DateTimeTask.objects.all().filter(pk=task['id'])
                datetimetask = datetimetask[0]
                datetimetask.taskstate = TaskState.objects.get(id=task['taskstate'])
                print("TASKSTATE")
                print datetimetask.taskstate
                datetimetask.last_run = datetime.datetime.now()
                datetimetask.set_repeats = datetimetask.set_repeats
                datetimetask.repeats = task["repeats"]
                datetimetask.set_datetime = datetimetask.set_datetime
                datetimetask.datetime = task["datetime"]
                datetimetask.created = datetimetask.created
                datetimetask.description = datetimetask.description
                datetimetask.label = datetimetask.label
                datetimetask.repetitions_done = int(datetimetask.set_repeats) - int(datetimetask.repeats)
                print "datetime.repetitions_done"
                print datetimetask.repetitions_done
                datetimetask_serialized = datetimetask
                datetimetask.taskfunction = datetimetask.taskfunction
                datetimetask.owner = datetimetask.owner
                datetimetask.device = datetimetask.device
            except DateTimeTask.DoesNotExist:
                datetimetask = DateTimeTask(**task)

            datetimetask.save()

        return JsonResponse({'status':True})


class DataTaskUpdateStateView(generic.View):

    #@method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        task = request.POST
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        if task:
            try:
                datatask = DataTask.objects.all().filter(pk=task['id'])
                datatask = datatask[0]
                datatask.taskstate = TaskState.objects.get(id=task['taskstate'])
                print("TASKSTATE")
                print datatask.taskstate
                datatask.last_run = datetime.datetime.now()
                print ("datatask.last_run")
                print (datatask.last_run)
                datatask.set_repeats = datatask.set_repeats
                datatask.repeats = task["repeats"]
                datatask.comparator = datatask.comparator
                datatask.data_value = datatask.data_value
                datatask.created = datatask.created
                datatask.description = datatask.description
                datatask.label = datatask.label
                datatask.repetitions_done = int(datatask.set_repeats) - int(datatask.repeats)
                datatask_serialized = datatask
                datatask.taskfunction = datatask.taskfunction
                datatask.owner = datatask.owner
                datatask.device = datatask.device

            except DataTask.DoesNotExist:
                raise
                datatask = DataTask(task)


            datatask.save()

        return JsonResponse({'status':True})
