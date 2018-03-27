# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import dateutil.parser as dp
import datetime
from calendar import monthrange
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Device, DeviceState
from data.models import Data
from django.views import generic
from django.contrib.auth.models import User
from django.conf import settings
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import Queue
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from elektron_django.mqtt import MqttClient
from django.db.models import Sum, Avg
from django.core import serializers

q = Queue.Queue()

def on_connect(client, userdata, flags, rc):
   print("Connected with result code "+str(rc))
   client.subscribe("data_to_web")

def on_message(client, userdata, msg):
   print "Sending data from MQTT(Device) to WebSocket(Web Interface)"
   data_json = ast.literal_eval(msg.payload)
   print data_json

   q.put(data_json)

class MqttClient(object):
    """docstring for MqttClient."""
    def __init__(self, client=mqtt.Client()):
        super(MqttClient, self).__init__()
        self.client = client
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect("localhost", 1883, 60)
        #self.client.connect("158.69.223.78", 1883, 60)

    def get_client(self):
        return self.client

    def set_on_connect(self, func):
        self.on_connect = func

    def publish(self, message, topic):
         print("Sending %s " % (message))
         self.client.publish(str(topic), message)
         return "Sending msg: %s " % (message)

def to_UTC(date):
    utc = settings.UTC
    if utc < 0:
        date = date - timedelta(hours=abs(utc))
    elif(utc >= 0):
        date = date + timedelta(hours=abs(utc))
    return date

def to_localtime(date):
    utc = settings.UTC
    if utc < 0:
        date = date + timedelta(hours=abs(utc))
    elif(utc >= 0):
        date = date - timedelta(hours=abs(utc))
    return date

def remove_data_nulls(data_list):
    for data in data_list:
        if data['data_value'] == None:
            data['data_value'] = 0
    return data_list

def check_device(**kwargs):

    if not 'device_ip' in kwargs:
        return False
    else:
        if type(kwargs['device_ip']) is list:
            kwargs['device_ip'] = kwargs['device_ip'][0]

    if not 'device_mac' in kwargs:
        return False
    else:
        if type(kwargs['device_mac']) is list:
            kwargs['device_mac'] = kwargs['device_mac'][0]

    if not 'label' in kwargs:
        #return false
        pass
    else:
        if type(kwargs['label']) is list:
            kwargs['label'] = kwargs['label'][0]

    if not 'devicestate' in kwargs:
        pass #return False
    else:
        if type(kwargs['devicestate']) is list:
            kwargs['devicestate'] = kwargs['devicestate'][0]

    try:
        kwargs['devicestate'] = DeviceState.objects.get(pk=kwargs['devicestate'])
    except Exception as e:
        #TODO: create default devicestates in settings.py
        kwargs['devicestate'] = DeviceState.objects.get(name="off")
        pass
    try:
        kwargs['owner'] = User.objects.get(username=kwargs['owner'])
    except Exception as e:
        #TODO: create default user in settings.py
        kwargs['owner'] = User.objects.get(username="root")

    return kwargs

def check_device_mac(**kwargs):
    if not 'device_mac' in kwargs:
        return False
    else:
        if type(kwargs['device_mac']) is list:
            kwargs['device_mac'] = kwargs['device_mac'][0]

    return kwargs

def to_json(**kwargs):

    if len(kwargs) == 2:
        pass
        #print "hay que convertir a dict"
    else:
        #print "hay que dejarlo igual"
        return kwargs


class IndexView(generic.ListView):
    model = Device

    def get(self, request, *args, **kwargs):
        """Return all devices."""

        pluged_devices = []
        last_data_list = []


        stateoff = DeviceState.objects.get(name="off")
        stateon = DeviceState.objects.get(name="on")
        #devices = list(map(lambda x: x.serialize(), Device.objects.all().filter(devicestate=stateon, enabled=True)))
        devices = Device.objects.all().filter(devicestate=stateon, enabled=True)

        for device in devices:
            device_data = {"device":"","lastdata":""}
            datehourago = datetime.datetime.now() - timedelta(minutes=15)
            data_query = Data.objects.all().filter(device=device, date__gte=datehourago)
            lastdata = Data.objects.all().filter(device=device)[0:20]
            if len(data_query) > 0:
                device.pluged = True
                device_obj = device.serialize()
                for data in lastdata:
                    last_data_list.insert(0,data.serialize())
                device_data = {"device":device_obj,"lastdata":last_data_list}
                pluged_devices.append(device_data)
            else:
                device.pluged = False
            device.save()

        """
        off_devices = Device.objects.all().filter(devicestate=stateoff)
        for device in off_devices:
                pluged_devices.append(device)

        disabled_devices = Device.objects.all().filter(enabled=False)
        for device in disabled_devices:
                pluged_devices.append(device)
        """
        print pluged_devices
        #pluged_devices = Device.objects.all().filter()

        return JsonResponse({'devices': pluged_devices})

class DetailView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):
        """Return the selected by id device."""
        try:
            data_list = []
            data_query = Data.objects.all().filter(device=kwargs["pk"])
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            #print data_list
            data_list = remove_data_nulls(data_list)[0:20]

            return JsonResponse({'device': Device.objects.get(id=kwargs["pk"]).serialize(), 'lastdata': data_list})
        except Exception as e:
            print "Some error ocurred getting Single Device with id: " + str(kwargs["pk"])
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DeviceByMac(generic.DetailView):
    model = Device

    def post(self, request, *args, **kwargs):
        """Return a Device by MAC"""
        result = request.POST
        try:
            device_mac = str(result["device_mac"]).encode("utf-8")
            device = Device.objects.get(device_mac=str(device_mac)).serialize()

            return JsonResponse({'device': device})
        except Exception as e:
            print "Some error ocurred getting Single Device by MAC"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DeviceDataView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []

            device = kwargs["pk"]
            data_query = Data.objects.all().filter(device=device)
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            #print data_list
            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DeviceDataOffsetLimitView(generic.DetailView):
    DEFAULT_LIMIT = 20
    DEFAULT_ORDER = 1
    DEFAULT_OFFSET = 1

    def get(self, request, *args, **kwargs):
        try:
            data_list = []
            offset = int(kwargs['offset'] if 'offset' in kwargs else self.DEFAULT_OFFSET) -1
            limit = int(kwargs['limit'] if 'limit' in kwargs else self.DEFAULT_LIMIT)
            order = kwargs['order'] if 'order' in kwargs else self.DEFAULT_ORDER

            device = kwargs["pk"]
            data_query = Data.objects.all().filter(device=device)[offset:limit]
            data_query = list(data_query)
            total_data = len(Data.objects.all().filter(device=device))

            for data in data_query:
                data_list.insert(0,data.serialize())

            return JsonResponse({'total_data': total_data,'data': data_list, 'pages': total_data / (limit - offset)})

        except Exception as e:
            print "Some error ocurred getting Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DeviceTotalData(generic.DetailView):

    def get(self, request, *args, **kwargs):
        try:
            device = kwargs["pk"]
            total_data = len(Data.objects.all().filter(device=device))

            return JsonResponse({'total_data': total_data})

        except Exception as e:
            print "Some error ocurred getting TotalData"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DeviceMacDataView(generic.DetailView):
    model = Device
    #template_name = 'device_data.html'

    def get(self, request, *args, **kwargs):
        device = Device()

        result = check_device_mac(**request.GET)

        if result:
            try:
                device_mac = result["device_mac"].replace(" ", "")
                device = Device.objects.get(device_mac=device_mac)

            except Exception as e:
                print  "Device you ask does not exist"
                print "Exception: " + str(e)
                return HttpResponse(status=500)

            if device:
                try:
                    data_list = []
                    data_query = Data.objects.all().filter(device=device)
                    data_query = list(data_query)

                    for data in data_query:
                        data_list.insert(0,data.serialize())

                    #print data_list
                    data_list = remove_data_nulls(data_list)
                    return JsonResponse({'data': data_list})

                except Exception as e:
                    print "Some error ocurred getting Device Data"
                    print "Exception: " + str(e)
                    return HttpResponse(status=500)

    def post(self, request, *args, **kwargs):
        device = Device()

        result = check_device_mac(**request.POST)

        if result:
            try:
                device = Device.objects.get(device_mac=result["device_mac"])

            except Exception as e:
                print  "Device you ask does not exist"
                print "Exception: " + str(e)
                return HttpResponse(status=500)

            if device:
                try:
                    data_list = []
                    data_query = Data.objects.all().filter(device=device)
                    data_query = list(data_query)

                    for data in data_query:
                        data_list.insert(0,data.serialize())

                    #print data_list
                    data_list = remove_data_nulls(data_list)
                    return JsonResponse({'data': data_list})

                except Exception as e:
                    print "Some error ocurred getting Device Data"
                    print "Exception: " + str(e)
                    return HttpResponse(status=500)


class DeviceTaskView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            task_list = []
            device = kwargs["pk"]
            task_query = Task.objects.all().filter(device=device)
            task_query = list(task_query)

            for task in task_query:
                task_list.insert(0,task.label)

            return JsonResponse({'task': task_list})

        except Exception as e:
            print "Some error ocurred getting Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DeviceMacTaskView(generic.DetailView):
    model = Device
    #template_name = 'device_data.html'

    def get(self, request, *args, **kwargs):
        print "GETDATA"
        print request.GET
        return JsonResponse({'status':True})

    def post(self, request, *args, **kwargs):
        device = Device()

        result = check_device_mac(**request.POST)

        if result:
            try:
                device = Device.objects.get(device_mac=result["device_mac"])

            except Exception as e:
                print  "Device you ask does not exist"
                print "Exception: " + str(e)
                return HttpResponse(status=500)

            if device:
                try:
                    task_list = []
                    task_query = Task.objects.all().filter(device=device)
                    task_query = list(task_query)

                    for task in task_query:
                        #print task
                        task_list.insert(0,task.task_value)

                    #print task_list
                    return JsonResponse({'task': task_list})

                except Exception as e:
                    print "Some error ocurred getting Device Task"
                    print "Exception: " + str(e)
                    return HttpResponse(status=500)

class DeviceDataDayView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            device = kwargs["pk"]

            day = kwargs["day"]
            month = kwargs["month"]
            year = kwargs["year"]

            date_string = day + "-" + month + "-" + year
            #date = dp.parse(date_string, timezone.now())
            date_from = datetime.datetime.strptime(date_string, "%d-%m-%Y").date()

            date_from = to_UTC(date_from) #TODO: Get timezone from country configured by user
            date_to = date_from + timedelta(hours=24)
            data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to)
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())


            #print data_list
            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Day Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DeviceDataMonthView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            device = kwargs["pk"]

            day = "1"
            month = kwargs["month"]
            year = kwargs["year"]
            cant_days_month = monthrange(int(year), int(month))[1]

            date_string = day + "-" + month + "-" + year
            #date = dp.parse(date_string, timezone.now())
            date_from = datetime.datetime.strptime(date_string, "%d-%m-%Y").date()

            date_to = date_from + timedelta(days=cant_days_month)
            data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to)
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())


            #print data_list
            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Month Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DeviceDataBetweenDaysView(generic.DetailView):
    DEFAULT_OFFSET = 1
    DEFAULT_LIMIT = 20
    DEFAULT_ORDER = 1

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            offset = int(kwargs['offset'] if 'offset' in kwargs else self.DEFAULT_OFFSET) -1
            limit = kwargs['limit'] if 'limit' in kwargs else self.DEFAULT_LIMIT
            order = kwargs['order'] if 'order' in kwargs else self.DEFAULT_ORDER

            device = kwargs["pk"]

            day1 = kwargs["day1"]
            month1 = kwargs["month1"]
            year1 = kwargs["year1"]

            day2 = kwargs["day2"]
            month2 = kwargs["month2"]
            year2 = kwargs["year2"]

            date_string1 = day1 + "-" + month1 + "-" + year1
            date_string2 = day2 + "-" + month2 + "-" + year2

            date_from = datetime.datetime.strptime(date_string1, "%d-%m-%Y").date()
            date_to = datetime.datetime.strptime(date_string2, "%d-%m-%Y").date()

            data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to)[offset:limit]
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            #print data_list
            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Between Days Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DeviceDataBetweenDaysPerhourView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            device = kwargs["pk"]

            day1 = kwargs["day1"]
            month1 = kwargs["month1"]
            year1 = kwargs["year1"]

            day2 = kwargs["day2"]
            month2 = kwargs["month2"]
            year2 = kwargs["year2"]

            datetime_string1 = day1 + "-" + month1 + "-" + year1 + " " + "00" + ":" + "00"
            datetime_string2 = day2 + "-" + month2 + "-" + year2 + " " + "23" + ":" + "59"

            date_from = datetime.datetime.strptime(datetime_string1, "%d-%m-%Y %H:%M")
            date_to = datetime.datetime.strptime(datetime_string2, "%d-%m-%Y %H:%M")

            date1 = date_from
            date2 = date_to

            diff = date2 - date1

            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600

            device_obj = Device.objects.get(pk=device)
            date_to = date_from + timedelta(hours=1)
            for hours_to in range(0,hours + 1):
                data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to).aggregate(data_perhoursum_hour=Sum('data_value'))
                dph = DataPH(data_query["data_perhoursum_hour"],device_obj,date_to)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=1)
                date_to = date_to + timedelta(hours=1)

            #print data_list
            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Between Days Per Hour Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DeviceDataBetweenDaysPerdayView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            device = kwargs["pk"]

            day1 = kwargs["day1"]
            month1 = kwargs["month1"]
            year1 = kwargs["year1"]

            day2 = kwargs["day2"]
            month2 = kwargs["month2"]
            year2 = kwargs["year2"]

            datetime_string1 = day1 + "-" + month1 + "-" + year1 + " " + "00" + ":" + "00"
            datetime_string2 = day2 + "-" + month2 + "-" + year2 + " " + "23" + ":" + "59"

            date_from = datetime.datetime.strptime(datetime_string1, "%d-%m-%Y %H:%M")#.date()
            date_to = datetime.datetime.strptime(datetime_string2, "%d-%m-%Y %H:%M")

            date1 = date_from
            date2 = date_to

            diff = date2 - date1

            days = diff.days

            device_obj = Device.objects.get(pk=device)
            date_to = date_from + timedelta(days=1)
            for hours_to in range(0,days):
                data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to).aggregate(data_perdaysum_day=Sum('data_value'))
                dph = DataPH(data_query["data_perdaysum_day"],device_obj,date_to)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=24)
                date_to = date_to + timedelta(hours=24)

            #print
            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Between Days Per Day Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)



class DeviceDataHourView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            device = kwargs["pk"]

            day = kwargs["day"]
            month = kwargs["month"]
            year = kwargs["year"]
            hour = kwargs["hour"]

            datetime_string = day + "-" + month + "-" + year + " " + hour + ":" + "00"
            #date = dp.parse(date_string, timezone.now())
            date_from = datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M")
            date_from = to_localtime(date_from) #TODO: Get timezone from country configured by user
            date_to = date_from + timedelta(minutes=59)

            data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to)
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            #print data_list
            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Hour Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DeviceDataBetweenHoursView(generic.DetailView):
    DEFAULT_LIMIT = 20
    DEFAULT_ORDER = 1
    DEFAULT_OFFSET = 1

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            offset = int(kwargs['offset'] if 'offset' in kwargs else self.DEFAULT_OFFSET) -1
            limit = int(kwargs['limit'] if 'limit' in kwargs else self.DEFAULT_LIMIT)
            order = kwargs['order'] if 'order' in kwargs else self.DEFAULT_ORDER

            device = kwargs["pk"]

            day1 = kwargs["day1"]
            month1 = kwargs["month1"]
            year1 = kwargs["year1"]
            hour1 = kwargs["hour1"]

            day2 = kwargs["day2"]
            month2 = kwargs["month2"]
            year2 = kwargs["year2"]
            hour2 = kwargs["hour2"]

            datetime_string1 = day1 + "-" + month1 + "-" + year1 + " " + hour1 + ":" + "00"
            datetime_string2 = day2 + "-" + month2 + "-" + year2 + " " + hour2 + ":" + "00"

            date_from = datetime.datetime.strptime(datetime_string1, "%d-%m-%Y %H:%M")
            date_to = datetime.datetime.strptime(datetime_string2, "%d-%m-%Y %H:%M")
            date_from = to_localtime(date_from)
            date_to = to_localtime(date_to)

            data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to)
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            #print data_list
            total_data = len(data_list)
            data_list = data_list[offset:limit]

            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list, 'total_data': total_data, 'pages': total_data / (limit - offset)})

        except Exception as e:
            print "Some error ocurred getting Between Hours Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DeviceDataBetweenHoursPerHourView(generic.DetailView):
    DEFAULT_LIMIT = 20
    DEFAULT_ORDER = 1
    DEFAULT_OFFSET = 1

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            offset = int(kwargs['offset'] if 'offset' in kwargs else self.DEFAULT_OFFSET) -1
            limit = int(kwargs['limit'] if 'limit' in kwargs else self.DEFAULT_LIMIT)
            order = kwargs['order'] if 'order' in kwargs else self.DEFAULT_ORDER

            device = kwargs["pk"]

            day1 = kwargs["day1"]
            month1 = kwargs["month1"]
            year1 = kwargs["year1"]
            hour1 = kwargs["hour1"]

            day2 = kwargs["day2"]
            month2 = kwargs["month2"]
            year2 = kwargs["year2"]
            hour2 = kwargs["hour2"]

            datetime_string1 = day1 + "-" + month1 + "-" + year1 + " " + hour1 + ":" + "00"
            datetime_string2 = day2 + "-" + month2 + "-" + year2 + " " + hour2 + ":" + "00"

            date_from = datetime.datetime.strptime(datetime_string1, "%d-%m-%Y %H:%M")
            date_to = datetime.datetime.strptime(datetime_string2, "%d-%m-%Y %H:%M")
            date_from = to_localtime(date_from)
            date_to = to_localtime(date_to)

            date1 = date_from
            date2 = date_to

            diff = date2 - date1

            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600

            device_obj = Device.objects.get(pk=device)
            date_to = date_from + timedelta(hours=1)
            for hours_to in range(0,hours + 1):
                data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to).aggregate(data_perhoursum_hour=Sum('data_value'))
                dph = DataPH(data_query["data_perhoursum_hour"],device_obj,date_to)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=1)
                date_to = date_to + timedelta(hours=1)

            #print data_list
            data_list = remove_data_nulls(data_list)

            total_data = len(data_list)
            data_list = data_list[offset:limit]

            return JsonResponse({'data': data_list, 'total_data': total_data, 'pages': total_data / (limit - offset)})

        except Exception as e:
            print "Some error ocurred getting Between Hours Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)



class DeviceDataBetweenHoursPerDayView(generic.DetailView):
    DEFAULT_LIMIT = 20
    DEFAULT_ORDER = 1
    DEFAULT_OFFSET = 1

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            offset = int(kwargs['offset'] if 'offset' in kwargs else self.DEFAULT_OFFSET) -1
            limit = int(kwargs['limit'] if 'limit' in kwargs else self.DEFAULT_LIMIT)
            order = kwargs['order'] if 'order' in kwargs else self.DEFAULT_ORDER

            device = kwargs["pk"]

            day1 = kwargs["day1"]
            month1 = kwargs["month1"]
            year1 = kwargs["year1"]
            hour1 = kwargs["hour1"]

            day2 = kwargs["day2"]
            month2 = kwargs["month2"]
            year2 = kwargs["year2"]
            hour2 = kwargs["hour2"]

            datetime_string1 = day1 + "-" + month1 + "-" + year1 + " " + hour1 + ":" + "00"
            datetime_string2 = day2 + "-" + month2 + "-" + year2 + " " + hour2 + ":" + "00"

            date_from = datetime.datetime.strptime(datetime_string1, "%d-%m-%Y %H:%M")
            date_to = datetime.datetime.strptime(datetime_string2, "%d-%m-%Y %H:%M")
            date_from = to_localtime(date_from)
            date_to = to_localtime(date_to)

            data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to)
            data_query = list(data_query)

            date1 = date_from
            date2 = date_to

            diff = date2 - date1

            days = diff.days

            device_obj = Device.objects.get(pk=device)
            date_to = date_from + timedelta(days=1)
            for hours_to in range(0,days):
                data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to).aggregate(data_perdaysum_day=Sum('data_value'))
                dph = DataPH(data_query["data_perdaysum_day"],device_obj,date_to)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=24)
                date_to = date_to + timedelta(hours=24)


            #print data_list
            data_list = remove_data_nulls(data_list)

            total_data = len(data_list)

            data_list = data_list[offset:limit]

            return JsonResponse({'data': data_list, 'total_data': total_data, 'pages': total_data / (limit - offset)})

        except Exception as e:
            print "Some error ocurred getting Between Hours Device Data"
            print "Exception: " + str(e)
            raise
            return HttpResponse(status=500)


class DeviceLastDataView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            device = kwargs["pk"]
            cant = kwargs["cant"]

            data_query = Data.objects.all().filter(device=device).order_by('-id')[:int(cant)]
            data_query = reversed(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Device Last Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DataPH(object):
    """docstring for DataPH."""
    def __init__(self, data, device, date):
        super(DataPH, self).__init__()
        self.data_value = data
        self.date = date
        self.device = device

    def set_device(self,device):
        self.device = device

    def set_date(self,date):
        self.date = date

    def __str__(self):
        return "Hour: " + str(self.hour) + " Data: " + str(self.data_value)

    def serialize(self):
        return {
            'data_value': self.data_value,
            'date' : self.date,
            'device': self.device.serialize()
        }

class DeviceDataDayPerHourView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            device = kwargs["pk"]
            day = kwargs["day"]
            month = kwargs["month"]
            year = kwargs["year"]

            datetime_string = day + "-" + month + "-" + year  + " " + "00" + ":" + "00"

            #date = dp.parse(date_string, timezone.now())

            date_from = datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M")
            date_from = to_localtime(date_from)
            date_from = to_UTC(date_from) #TODO: Get timezone from country configured by user

            device_obj = Device.objects.get(pk=device)
            date_to = date_from + timedelta(hours=1)
            for hours_to in range(1,24):
                data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to).aggregate(data_perhoursum_hour=Sum('data_value'))
                dph = DataPH(data_query["data_perhoursum_hour"],device_obj,date_to)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=1)
                date_to = date_to + timedelta(hours=1)

            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Device Data Per Hour"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DeviceDataMonthPerHourView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            device = kwargs["pk"]

            day = "1"
            month = kwargs["month"]
            year = kwargs["year"]
            cant_days_month = monthrange(int(year), int(month))[1]

            datetime_string = day + "-" + month + "-" + year  + " " + "00" + ":" + "00"

            date_from = datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M")#.date()
            date_to = date_from + timedelta(days=cant_days_month)

            date1 = date_from
            date2 = date_to

            diff = date2 - date1

            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600

            device_obj = Device.objects.get(pk=device)
            date_to = date_from + timedelta(hours=1)
            for hours_to in range(1,hours):
                data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to).aggregate(data_perhoursum_hour=Sum('data_value'))
                dph = DataPH(data_query["data_perhoursum_hour"],device_obj,date_to)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=1)
                date_to = date_to + timedelta(hours=1)

            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Device Data Per Hour"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DeviceDataPerHourView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            device = kwargs["pk"]
            device_obj = Device.objects.get(pk=device)
            device_year = device_obj.created.year
            device_month = device_obj.created.month
            device_day = device_obj.created.day

            day = str(device_day)
            month = str(device_month)
            year = str(device_year)

            datetime_string = day + "-" + month + "-" + year  + " " + "00" + ":" + "00"

            date_from = datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M")#.date()
            date_to = datetime.datetime.now()

            date1 = date_from
            date2 = date_to

            diff = date2 - date1

            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600


            date_to = date_from + timedelta(hours=1)
            for hours_to in range(1,hours):
                data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to).aggregate(data_perhoursum_hour=Sum('data_value'))
                dph = DataPH(data_query["data_perhoursum_hour"],device_obj,date_to)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=1)
                date_to = date_to + timedelta(hours=1)

            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Device Data Per Hour"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DeviceDataMonthPerDayView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            device = kwargs["pk"]

            day = "1"
            month = kwargs["month"]
            year = kwargs["year"]
            cant_days_month = monthrange(int(year), int(month))[1]

            datetime_string = day + "-" + month + "-" + year  + " " + "00" + ":" + "00"

            date_from = datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M")#.date()

            device_obj = Device.objects.get(pk=device)
            date_to = date_from + timedelta(days=1)
            for hours_to in range(1,cant_days_month):
                data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to).aggregate(data_perdaysum_day=Sum('data_value'))
                dph = DataPH(data_query["data_perdaysum_day"],device_obj,date_from)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=24)
                date_to = date_to + timedelta(hours=24)

            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Device Data Per Hour"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DeviceDataPerDayView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []

            device = kwargs["pk"]
            device_obj = Device.objects.get(pk=device)
            device_year = device_obj.created.year
            device_month = device_obj.created.month
            device_day = device_obj.created.day

            day = str(device_day)
            month = str(device_month)
            year = str(device_year)
            cant_days_month = monthrange(int(year), int(month))[1]

            datetime_string = day + "-" + month + "-" + year  + " " + "00" + ":" + "00"

            date_from = datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M")#.date()
            date_to = datetime.datetime.now()

            date1 = date_from
            date2 = date_to

            diff = date2 - date1

            days = diff.days

            date_from = datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M")#.date()

            device_obj = Device.objects.get(pk=device)
            date_to = date_from + timedelta(days=1)
            for hours_to in range(1,days):
                data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to).aggregate(data_perdaysum_day=Sum('data_value'))
                dph = DataPH(data_query["data_perdaysum_day"],device_obj,date_from)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=24)
                date_to = date_to + timedelta(hours=24)


            data_list = remove_data_nulls(data_list)
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Device Data Per Day"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class RecognitionView(generic.View):

    def post(self, request):
        return JsonResponse({'status':True})

class DeviceDelete(DeleteView):

    def post(self, request, *args, **kwargs):
        result = check_device(**request.POST)

        if result:
            try:
                device = Device.objects.get(device_mac=str(result["device_mac"]))

            except Device.DoesNotExist:
                message = "Device does not exists!"
                response = JsonResponse({'status':'false','message':message}, status=500)
                return JsonResponse(response)

            device.delete()

        return JsonResponse({'status':True})

class CreateView(generic.View):

    def post(self, request, *args, **kwargs):
        result = check_device(**request.POST)

        if result:
            try:
                device = Device.objects.get(device_mac=str(result["device_mac"]))
                device.device_ip = device["device_ip"]
                device.label = device["label"]
                device.devicestate = device["devicestate"]

            except Device.DoesNotExist:
                try:
                    if result["data_value"]:
                        del result["data_value"]
                except Exception as e:
                    pass
                device = Device(**result)
            device.save()


        return JsonResponse({'status':True})


class UpdateView(generic.View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        result = check_device(**request.POST)

        if result:
            try:
                device = Device.objects.get(device_mac=result["device_mac"])
                device.device_ip = result["device_ip"]
                device.label = result["label"]
                device.devicestate = result["devicestate"]

            except Device.DoesNotExist:
                device = Device(**result)

            device.save()

        return JsonResponse({'status':True})

class ShutdownView(generic.View):

    def get(self, request, *args, **kwargs):
        device_pk = kwargs["pk"]

        if device_pk:
            try:
                device = Device.objects.get(pk=device_pk)
                mini_mac = device.device_mac[-5:]

                if str(device.devicestate) == "on":
                    topic = "elektron/"+str(mini_mac)+"/new_order"
                    order = 1
                    device.devicestate = DeviceState.objects.get(name="off")
                    device.last_state_date_off = datetime.datetime.now()
                    device.state_counter_off += 1
                    device.save()
                    mqtt = MqttClient()
                    mqtt.publish(order, topic)

            except Device.DoesNotExist:
                print "Some error ocurred shutting downd Single Device with id: " + str(kwargs["pk"])
                print "No such device"
                print "Exception: " + str(e)
                return HttpResponse(status=500)

            device.save()

        return JsonResponse({'status':True})


    def post(self, request, *args, **kwargs):
        result = check_device(**request.POST)

        if result:
            try:
                device = Device.objects.get(device_mac=result["device_mac"])
                device.device_ip = result["device_ip"]
                device.label = result["label"]
                mini_mac = device.device_mac[-5:]

                if str(device.devicestate) == "on":
                    topic = "elektron/"+str(mini_mac)+"/new_order"
                    order = 1
                    device.devicestate = DeviceState.objects.get(name="off")
                    device.last_state_date_off = datetime.datetime.now()
                    device.state_counter_off += 1
                    mqtt = MqttClient()
                    mqtt.publish(order, topic)

            except Device.DoesNotExist:
                print "Some error ocurred shutting downd Single Device with id: " + str(kwargs["pk"])
                print "No such device"
                print "Exception: " + str(e)
                return HttpResponse(status=500)

            device.save()

        return JsonResponse({'status':True})


class TurnonView(generic.View):

    def get(self, request, *args, **kwargs):
        device_pk = kwargs["pk"]

        if device_pk:
            try:
                device = Device.objects.get(pk=device_pk)
                mini_mac = device.device_mac[-5:]

                if str(device.devicestate) == "off":
                    topic = "elektron/"+str(mini_mac)+"/new_order"
                    order = 0
                    device.devicestate = DeviceState.objects.get(name="on")
                    device.last_state_date_on = datetime.datetime.now()
                    device.state_counter_on += 1
                    mqtt = MqttClient()
                    mqtt.publish(order, topic)

            except Device.DoesNotExist:
                print "Some error ocurred shutting downd Single Device with id: " + str(kwargs["pk"])
                print "No such device"
                print "Exception: " + str(e)
                return HttpResponse(status=500)

            device.save()

        return JsonResponse({'status':True})

    def post(self, request, *args, **kwargs):

        result = check_device(**request.POST)

        if result:
            try:
                device = Device.objects.get(device_mac=result["device_mac"])
                device.device_ip = result["device_ip"]
                device.label = result["label"]
                mini_mac = device.device_mac[-5:]

                if str(device.devicestate) == "off":
                    topic = "elektron/"+str(mini_mac)+"/new_order"
                    order = 0
                    device.devicestate = DeviceState.objects.get(name="on")
                    device.last_state_date_on = datetime.datetime.now()
                    device.state_counter_on += 1
                    mqtt = MqttClient()
                    mqtt.publish(order, topic)

            except Device.DoesNotExist:
                print "Some error ocurred shutting downd Single Device with id: " + str(kwargs["pk"])
                print "No such device"
                print "Exception: " + str(e)
                return HttpResponse(status=500)

            device.save()

        return JsonResponse({'status':True})

class UpdateLabelView(generic.View):

    def post(self, request, *args, **kwargs):

        try:

            device_pk = kwargs["pk"]
            new_label = request.POST['label']
            device = Device.objects.get(pk=device_pk)
            #mini_mac = device.device_mac[-5:]

            #topic = "elektron/"+str(mini_mac)+"/new_order"
            #new_label = str(request["label"])
            device.label = new_label
            #mqtt = MqttClient()
            #mqtt.publish(new_label, topic)
            #print "device.label"
            #print device.label

        except Device.DoesNotExist:
            print "Some error ocurred shutting downd Single Device with id: " + str(kwargs["pk"])
            print "No such device"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

        device.save()

        return JsonResponse({'status':True})

class UpdateIpView(generic.View):

    def post(self, request, *args, **kwargs):

        try:

            device_mac = request.POST["device_mac"]
            new_ip = request.POST['device_ip']
            device = Device.objects.get(device_mac=device_mac)
            device.device_ip = new_ip


        except Device.DoesNotExist:
            print "Some error ocurred shutting downd Single Device with id: " + str(kwargs["pk"])
            print "No such device"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

        device.save()

        return JsonResponse({'status':True})


class EnableView(generic.View):

    def post(self, request, *args, **kwargs):

        try:
            device_pk = kwargs["pk"]
            device = Device.objects.get(pk=device_pk)
            device.enabled = True

        except Device.DoesNotExist:
            device = Device(**result)

        device.save()

        return JsonResponse({'status':True})

class DisableView(generic.View):

    def post(self, request, *args, **kwargs):

        try:
            device_pk = kwargs["pk"]
            device = Device.objects.get(pk=device_pk)
            device.enabled = False

        except Device.DoesNotExist:
            device = Device(**result)

        device.save()

        return JsonResponse({'status':True})

def percent(num1, num2):
    num1 = float(num1)
    num2 = float(num2)
    percentage = '{0:.2f}'.format((num1 / num2 * 100))
    return percentage

class DeviceStatisticsView(generic.DetailView):
    model = Device
    """
    - ID componente
    - Nombre componente
    - Estado (encendido/apagado)

    - Consumo total historico
    - Consumo promedio historico:
        - Por hora
        - Por día
        - Por mes
    - Ultima medicion
    - Tiempo del ultimo periodo de actividad en minutos/horas
    - Consumo del último periodo de actividad total
    - Consumo promedio del último periodo de actividad
    - Cantidad de encendidos y apagados históricos
    """
    def get(self, request, *args, **kwargs):

        try:
            data_list = []

            device = kwargs["pk"]
            device = Device.objects.all().filter(id=device)
            data_query = Data.objects.all().filter(device=device)
            data_query = list(data_query)

            device = device[0].serialize()

            data_sum_query = Data.objects.all().filter(device= device['id']).aggregate(data_sum=Sum('data_value'))

            date_from = device["created"]
            date_to = datetime.datetime.now()

            date1 = date_from
            date2 = date_to

            diff = date2 - date1

            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600

            device_data_sum = data_sum_query['data_sum']

            if data_sum == None or data_sum == 0:
                device_data_sum = 0
            else:
                prom_hours = device_data_sum / hours
                prom_days = device_data_sum / days

            data_avg_query = Data.objects.all().filter(device= device['id']).aggregate(data_avg=Avg('data_value'))
            data_avg = data_avg_query['data_avg']

            last_data_query = Data.objects.all().filter(device= device['id'])
            last_data = list(last_data_query)[-1]
            last_data_date = last_data.serialize()['date']
            last_data = float(last_data.serialize()['data_value'])

            last_state_date_on = device['last_state_date_on']
            last_state_date_off = device['last_state_date_off']
            state_counter_on = device['state_counter_on']
            state_counter_off = device['state_counter_off']

            date_from = device['last_state_date_on']
            date_to = device['last_state_date_off']
            if date_to < date_from:
                date_to = datetime.datetime.now()

            data_query_avg_states = Data.objects.all().filter(device=device['id'], date__gte=date_from, date__lte=date_to).aggregate(data_avg_states=Avg('data_value'))
            data_avg_states = data_query_avg_states['data_avg_states']

            data_query_sum_states = Data.objects.all().filter(device=device['id'], date__gte=date_from, date__lte=date_to).aggregate(data_sum_states=Sum('data_value'))
            data_sum_states = data_query_sum_states['data_sum_states']

            all_devices_sum = Data.objects.all().aggregate(all_devices_sum=Sum('data_value'))

            all_devices_sum = all_devices_sum["all_devices_sum"]
            device_percent = (device_data_sum * 100) /  all_devices_sum

            co2_porcent = 35
            device_co2 = ((device_data_sum / 1000) * co2_porcent) / 100

            total_co2 = ((all_devices_sum / 1000) * co2_porcent) / 100

            edelap_marzo18 = 0.002779432624113475
            device_tarifa = device_data_sum * edelap_marzo18
            total_tarifa = all_devices_sum * edelap_marzo18

            #return JsonResponse({'device': device, 'data_sum': data_sum, 'days_created': days, 'hours_created':hours, 'prom_days': prom_days, 'prom_hours':prom_hours, 'prom_total': data_avg })
            return JsonResponse({'device': device, 'device_tarifa':device_tarifa, 'total_tarifa':total_tarifa,  'device_co2': device_co2, 'total_co2': total_co2, 'device_percent':device_percent ,'device_data_sum': device_data_sum, 'all_data_sum': all_devices_sum, 'days_created': days, 'hours_created':hours, 'prom_total': data_avg, 'last_data': { 'value': last_data, 'date':last_data_date}, 'data_list_avg_states': data_avg_states, 'data_list_sum_states': data_sum_states })


        except Exception as e:
            print "Some error ocurred getting Device Data"
            print "Exception: " + str(e)
            raise
            return HttpResponse(status=500)


class StatisticsView(generic.DetailView):
    model = Device
    """
    - ID componente
    - Nombre componente
    - Estado (encendido/apagado)

    - Consumo total historico
    - Consumo promedio historico:
        - Por hora
        - Por día
        - Por mes
    - Ultima medicion
    - Tiempo del ultimo periodo de actividad en minutos/horas
    - Consumo del último periodo de actividad total
    - Consumo promedio del último periodo de actividad
    - Cantidad de encendidos y apagados históricos
    """
    def get(self, request, *args, **kwargs):

        try:
            device_list = []

            devices = Device.objects.all()

            for device in devices:

                data_list = []

                data_query = Data.objects.all().filter(device=device)
                data_query = list(data_query)

                device = device.serialize()

                data_sum_query = Data.objects.all().filter(device= device['id']).aggregate(data_sum=Sum('data_value'))

                date_from = device["created"]
                date_to = datetime.datetime.now()

                date1 = date_from
                date2 = date_to

                diff = date2 - date1

                days, seconds = diff.days, diff.seconds
                hours = days * 24 + seconds // 3600

                data_sum = data_sum_query['data_sum']

                if data_sum == None or data_sum == 0:
                    data_sum = 0
                else:
                    prom_hours = data_sum / hours
                    prom_days = data_sum / days

                data_avg_query = Data.objects.all().filter(device= device['id']).aggregate(data_avg=Avg('data_value'))
                data_avg = data_avg_query['data_avg']

                last_data = None
                if len(data_query) > 0:
                    last_data_query = Data.objects.all().filter(device= device['id'])
                    last_data = list(last_data_query)[-1]
                    last_data_date = last_data.serialize()['date']
                    last_data = float(last_data.serialize()['data_value'])
                else:
                    last_data_date = ""

                last_state_date_on = device['last_state_date_on']
                last_state_date_off = device['last_state_date_off']
                state_counter_on = device['state_counter_on']
                state_counter_off = device['state_counter_off']

                date_from = device['last_state_date_on']
                date_to = device['last_state_date_off']
                if date_to < date_from:
                    date_to = datetime.datetime.now()

                data_query_avg_states = Data.objects.all().filter(device=device['id'], date__gte=date_from, date__lte=date_to).aggregate(data_avg_states=Avg('data_value'))
                data_avg_states = data_query_avg_states['data_avg_states']

                data_query_sum_states = Data.objects.all().filter(device=device['id'], date__gte=date_from, date__lte=date_to).aggregate(data_sum_states=Sum('data_value'))
                data_sum_states = data_query_sum_states['data_sum_states']

                co2_porcent = 35
                device_co2 = ((data_sum / 1000) * co2_porcent) / 100
                total_co2 = ((data_sum / 1000) * co2_porcent) / 100

                edelap_marzo18 = 0.002779432624113475
                device_tarifa = data_sum * edelap_marzo18
                total_tarifa = data_sum * edelap_marzo18

                device_data = {'device': device, 'data_sum': data_sum, 'device_tarifa':device_tarifa, 'total_tarifa':total_tarifa,  'device_co2': device_co2, 'total_co2': total_co2, 'days_created': days, 'hours_created':hours, 'prom_total': data_avg, 'last_data': { 'value': last_data, 'date':last_data_date}, 'data_list_avg_states': data_avg_states, 'data_list_sum_states': data_sum_states }
                device_list.append(device_data)

            return JsonResponse({"devices": device_list})

        except Exception as e:
            print "Some error ocurred getting Device Data"
            print "Exception: " + str(e)
            raise
            return HttpResponse(status=500)
