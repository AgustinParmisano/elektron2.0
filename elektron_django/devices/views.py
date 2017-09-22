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
        return False
    else:
        if type(kwargs['label']) is list:
            kwargs['label'] = kwargs['label'][0]

    if not 'devicestate' in kwargs:
        return False
    else:
        if type(kwargs['devicestate']) is list:
            kwargs['devicestate'] = kwargs['devicestate'][0]

    try:
        kwargs['devicestate'] = DeviceState.objects.get(pk=kwargs['devicestate'])
    except Exception as e:
        #TODO: create default devicestates in settings.py
        kwargs['devicestate'] = DeviceState.objects.get(name="off")
        raise
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


class IndexView(generic.ListView):
    model = Device

    def get(self, request, *args, **kwargs):
        """Return all devices."""
        return JsonResponse({'devices': list(map(lambda x: x.serialize(), Device.objects.all()))})

class DetailView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):
        """Return the selected by id device."""
        try:
            return JsonResponse({'device': Device.objects.get(id=kwargs["pk"]).serialize()})
        except Exception as e:
            print "Some error ocurred getting Single Device with id: " + str(kwargs["pk"])
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
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Device Data"
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
                #print task
                task_list.insert(0,task.label)

            #print task_list
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
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Month Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DeviceDataBetweenDaysView(generic.DetailView):
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

            date_string1 = day1 + "-" + month1 + "-" + year1
            date_string2 = day2 + "-" + month2 + "-" + year2

            date_from = datetime.datetime.strptime(date_string1, "%d-%m-%Y").date()
            date_to = datetime.datetime.strptime(date_string2, "%d-%m-%Y").date()

            data_query = Data.objects.all().filter(device=device, date__gte=date_from, date__lte=date_to)
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            #print data_list
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Between Days Device Data"
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
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Hour Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DeviceDataBetweenHoursView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
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
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Between Hours Device Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class RecognitionView(generic.View):

    def post(self, request):
        return JsonResponse({'status':True})

class CreateView(generic.View):

    def post(self, request, *args, **kwargs):

        result = check_device(**request.POST)

        if result:
            try:
                device = Device.objects.get(device_mac=result["device_mac"])
                device.device_ip = result["device_ip"]
                device.label = result["label"]
                device.devicestate = result["devicestate"]

            except Device.DoesNotExist:
                if result["data_value"]:
                    del result["data_value"]
                device = Device(**result)

            device.save()

        return JsonResponse({'status':True})


class UpdateView(generic.View):

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
