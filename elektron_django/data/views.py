# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import dateutil.parser as dp
import datetime
import pytz
from calendar import monthrange
from datetime import timedelta
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from devices.models import Device, DeviceState
from .models import Data
from django.views import generic
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum, Avg
from django.core import serializers

def watts_tax_co2_converter(watts):
    co2_porcent = 35
    total_co2 = ((watts / 1000) * co2_porcent) / 100

    edelap_marzo18 = 0.002779432624113475
    total_tax = watts * edelap_marzo18

    return {'total_watts': watts, 'total_tax': total_tax, 'total_co2': total_co2}

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
    """
    try:
        kwargs['devicestate'] = DeviceState.objects.get(id=kwargs['devicestate'])
    except Exception as e:
        #TODO: create default devicestates in settings.py
        kwargs['devicestate'] = DeviceState.objects.get(name="off")

    try:
        kwargs['owner'] = User.objects.get(username=kwargs['owner'])
    except Exception as e:
        #TODO: create default user in settings.py
        kwargs['owner'] = User.objects.get(username="root")
    """
    return kwargs

def check_data(**kwargs):

    if not 'data_value' in kwargs:
        return False
    else:
        if type(kwargs['data_value']) is list:
            kwargs['data_value'] = kwargs['data_value'][0]

    return kwargs

class DataPH(object):
    """docstring for DataPH."""
    def __init__(self, data, date):
        super(DataPH, self).__init__()
        self.data_value = data
        self.date = date

    def set_date(self,date):
        self.date = date

    def __str__(self):
        return "Hour: " + str(self.hour) + " Data: " + str(self.data_value)

    def serialize(self):
        return {
            'data_value': self.data_value,
            'date' : self.date,
        }

class GetDataWattsTaxCo2(generic.DetailView):

    def get(self, request, *args, **kwargs):
        try:
            total_data =  Data.objects.all().aggregate(all_devices_sum=Sum('data_value'))
            data = watts_tax_co2_converter(total_data["all_devices_sum"])

            return JsonResponse({'total_watts': data["total_watts"],'total_tax': data["total_tax"],'total_co2': data["total_co2"]})

        except Exception as e:
            print "Some error ocurred getting GetDataWattsTaxCo2"
            print "Exception: " + str(e)
            raise
            return HttpResponse(status=500)

class DataDayPerHourView(generic.DetailView):
    model = Data

    def get(self, request, *args, **kwargs):

        try:
            data_list = []
            day = kwargs["day"]
            month = kwargs["month"]
            year = kwargs["year"]

            datetime_string = day + "-" + month + "-" + year  + " " + "00" + ":" + "00"

            #date = dp.parse(date_string, timezone.now())

            date_from = datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M")

            date_to = date_from + timedelta(hours=1)
            print date_from
            print date_to
            for hours_to in range(1,24):
                data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to).aggregate(data_perhoursum_hour=Sum('data_value'))
                dph = DataPH(data_query["data_perhoursum_hour"],date_to)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=1)
                date_to = date_to + timedelta(hours=1)

            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Data Day Per Hour"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DataMonthPerHourView(generic.DetailView):
    model = Data

    def get(self, request, *args, **kwargs):

        try:
            data_list = []

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

            date_to = date_from + timedelta(hours=1)
            for hours_to in range(1,hours):
                data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to).aggregate(data_perhoursum_hour=Sum('data_value'))
                dph = DataPH(data_query["data_perhoursum_hour"],date_to)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=1)
                date_to = date_to + timedelta(hours=1)

            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Data Month Per Hour"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DataPerHourView(generic.DetailView):
    model = Data

    def get(self, request, *args, **kwargs):

        try:
            data_list = []

            day = "1"
            month = "1"
            year = "2017"

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
                data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to).aggregate(data_perhoursum_hour=Sum('data_value'))
                dph = DataPH(data_query["data_perhoursum_hour"],date_to)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=1)
                date_to = date_to + timedelta(hours=1)

            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Data Per Hour"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class GetDataOffsetLimit(generic.DetailView):
    DEFAULT_OFFSET = 1
    DEFAULT_LIMIT = 20
    DEFAULT_ORDER = 1

    def get(self, request, *args, **kwargs):
        try:
            data_list = []
            offset = kwargs['offset'] if 'offset' in kwargs else self.DEFAULT_OFFSET
            offset = int(offset) - 1
            limit = kwargs['limit'] if 'limit' in kwargs else self.DEFAULT_LIMIT
            order = kwargs['order'] if 'order' in kwargs else self.DEFAULT_ORDER

            data_query = Data.objects.all()[offset:limit]
            total_data = len(Data.objects.all())

            for data in data_query:
                data_list.insert(0,data.serialize())

            if int(order) > 1:
                data_list = list(reversed(data_list))

            return JsonResponse({'total_data': total_data,'data': data_list})

        except Exception as e:
            print "Some error ocurred getting DataOffsetLimit"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class GetTotalData(generic.DetailView):

    def get(self, request, *args, **kwargs):
        try:
            total_data = len(Data.objects.all())

            return JsonResponse({'total_data': total_data})

        except Exception as e:
            print "Some error ocurred getting TotalData"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DataBetweenDaysPerhourView(generic.DetailView):
    model = Data

    def get(self, request, *args, **kwargs):

        try:
            data_list = []

            day1 = kwargs["day1"]
            month1 = kwargs["month1"]
            year1 = kwargs["year1"]

            day2 = kwargs["day2"]
            month2 = kwargs["month2"]
            year2 = kwargs["year2"]

            datetime_string1 = day1 + "-" + month1 + "-" + year1 + " " + "00" + ":" + "00"
            datetime_string2 = day2 + "-" + month2 + "-" + year2 + " " + "00" + ":" + "00"

            date_from = datetime.datetime.strptime(datetime_string1, "%d-%m-%Y %H:%M")#.date()
            date_to = datetime.datetime.strptime(datetime_string2, "%d-%m-%Y %H:%M")#.date()

            date1 = date_from
            date2 = date_to

            diff = date2 - date1

            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600

            date_to = date_from + timedelta(hours=1)
            for hours_to in range(1,hours):
                data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to).aggregate(data_perhoursum_hour=Sum('data_value'))
                dph = DataPH(data_query["data_perhoursum_hour"],date_to)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=1)
                date_to = date_to + timedelta(hours=1)

            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Data Between Days Per Hour"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DataPerDayView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):

        try:
            data_list = []

            day = "1"
            month = "1"
            year = "2017"

            datetime_string = day + "-" + month + "-" + year  + " " + "00" + ":" + "00"

            date_from = datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M")#.date()
            date_to = datetime.datetime.now()

            date1 = date_from
            date2 = date_to

            diff = date2 - date1

            days = diff.days

            date_from = datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M")#.date()

            date_to = date_from + timedelta(days=1)
            for hours_to in range(0,days + 1):
                data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to).aggregate(data_perdaysum_day=Sum('data_value'))
                dph = DataPH(data_query["data_perdaysum_day"],date_from)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=24)
                date_to = date_to + timedelta(hours=24)

            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Data Per Day"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DataBetweenDaysPerdayView(generic.DetailView):
    model = Device

    def get(self, request, *args, **kwargs):
        try:
            data_list = []

            day1 = kwargs["day1"]
            month1 = kwargs["month1"]
            year1 = kwargs["year1"]

            day2 = kwargs["day2"]
            month2 = kwargs["month2"]
            year2 = kwargs["year2"]

            datetime_string1 = day1 + "-" + month1 + "-" + year1 + " " + "00" + ":" + "00"
            datetime_string2 = day2 + "-" + month2 + "-" + year2 + " " + "00" + ":" + "00"

            date_from = datetime.datetime.strptime(datetime_string1, "%d-%m-%Y %H:%M")#.date()
            date_to = datetime.datetime.strptime(datetime_string2, "%d-%m-%Y %H:%M")#.date()

            date1 = date_from
            date2 = date_to

            diff = date2 - date1

            days = diff.days

            date_to = date_from + timedelta(days=1)
            for hours_to in range(0,days + 1):
                data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to).aggregate(data_perdaysum_day=Sum('data_value'))
                dph = DataPH(data_query["data_perdaysum_day"],date_from)
                data_list.insert(0,dph.serialize())
                date_from = date_from + timedelta(hours=24)
                date_to = date_to + timedelta(hours=24)

            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Data Per Day"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class IndexView(generic.DetailView):
    model = Data

    def get(self, request, *args, **kwargs):
        """Return all data."""
        return JsonResponse({'data': list(map(lambda x: x.serialize(), Data.objects.all()))})

class DetailView(generic.DetailView):
    model = Data

    def get(self, request, *args, **kwargs):
        """Return the last published data."""
        try:
            return JsonResponse({'data': Data.objects.get(id=kwargs["pk"]).serialize()})
        except Exception as e:
            print "Some error ocurred getting Single Data with id: " + str(kwargs["pk"])
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DataDayView(generic.DetailView):
    model = Data

    def get(self, request, *args, **kwargs):

        try:
            data_list = []

            day = kwargs["day"]
            month = kwargs["month"]
            year = kwargs["year"]

            date_string = day + "-" + month + "-" + year

            date_from = datetime.datetime.strptime(date_string, "%d-%m-%Y").date()

            date_from = to_localtime(date_from) #TODO: Get timezone from country configured by user
            date_to = date_from + timedelta(hours=24)

            data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to)
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Day Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DataMonthView(generic.DetailView):
    model = Data

    def get(self, request, *args, **kwargs):

        try:
            data_list = []

            day = "1"
            month = kwargs["month"]
            year = kwargs["year"]
            cant_days_month = monthrange(int(year), int(month))[1]

            date_string = day + "-" + month + "-" + year
            #date = dp.parse(date_string, timezone.now())
            date_from = datetime.datetime.strptime(date_string, "%d-%m-%Y").date()
            date_to = date_from + timedelta(days=cant_days_month)
            data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to)
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            #print data_list
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Month Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DataBetweenDaysView(generic.DetailView):
    model = Data

    def get(self, request, *args, **kwargs):

        try:
            data_list = []

            day1 = kwargs["day1"]
            month1 = kwargs["month1"]
            year1 = kwargs["year1"]

            day2 = kwargs["day2"]
            month2 = kwargs["month2"]
            year2 = kwargs["year2"]

            date_string1 = day1 + "-" + month1 + "-" + year1
            date_string2 = day2 + "-" + month2 + "-" + year2

            #date = dp.parse(date_string, timezone.now())
            date_from = datetime.datetime.strptime(date_string1, "%d-%m-%Y").date()
            date_to = datetime.datetime.strptime(date_string2, "%d-%m-%Y").date()

            data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to)
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            #print data_list
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Between Days Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DataBetweenDaysPostView(generic.DetailView):
    model = Data

    def post(self, request, *args, **kwargs):

        try:
            postdata = request.POST
            data_list = []

            day1 = postdata["day1"]
            month1 = postdata["month1"]
            year1 = postdata["year1"]

            day2 = postdata["day2"]
            month2 = postdata["month2"]
            year2 = postdata["year2"]

            if "device_id" in postdata:
                device_id = postdata["device_id"]
            else:
                device_id = ""

            date_string1 = day1 + "-" + month1 + "-" + year1
            date_string2 = day2 + "-" + month2 + "-" + year2

            #date = dp.parse(date_string, timezone.now())
            date_from = datetime.datetime.strptime(date_string1, "%d-%m-%Y").date()
            date_to = datetime.datetime.strptime(date_string2, "%d-%m-%Y").date()

            if device_id:
                data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to, device=device_id)
            else:
                data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to)

            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            #print data_list
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Between Days Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DataHourView(generic.DetailView):
    model = Data

    def get(self, request, *args, **kwargs):

        try:
            data_list = []

            day = kwargs["day"]
            month = kwargs["month"]
            year = kwargs["year"]
            hour = kwargs["hour"]

            datetime_string = day + "-" + month + "-" + year + " " + hour + ":" + "00"
            #date = dp.parse(date_string, timezone.now())
            date_from = datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M")
            date_from = to_localtime(date_from) #TODO: Get timezone from country configured by user
            date_to = date_from + timedelta(minutes=59)

            data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to)
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            #print data_list
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Hour Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)

class DataBetweenHoursView(generic.DetailView):
    model = Data

    def get(self, request, *args, **kwargs):

        try:
            data_list = []

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

            data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to)
            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            #print data_list
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Between Hour Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)


class DataBetweenHoursPostView(generic.DetailView):
    model = Data

    def post(self, request, *args, **kwargs):

        try:
            postdata = request.POST
            data_list = []


            day1 = postdata["day1"]
            month1 = postdata["month1"]
            year1 = postdata["year1"]
            hour1 = postdata["hour1"]

            day2 = postdata["day2"]
            month2 = postdata["month2"]
            year2 = postdata["year2"]
            hour2 = postdata["hour2"]

            if "device_id" in postdata:
                device_id = postdata["device_id"]
            else:
                device_id = ""

            datetime_string1 = day1 + "-" + month1 + "-" + year1 + " " + hour1 + ":" + "00"
            datetime_string2 = day2 + "-" + month2 + "-" + year2 + " " + hour2 + ":" + "00"

            date_from = datetime.datetime.strptime(datetime_string1, "%d-%m-%Y %H:%M")
            date_to = datetime.datetime.strptime(datetime_string2, "%d-%m-%Y %H:%M")
            date_from = to_localtime(date_from)
            date_to = to_localtime(date_to)

            if device_id:
                data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to, device=device_id)
            else:
                data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to)

            data_query = list(data_query)

            for data in data_query:
                data_list.insert(0,data.serialize())

            #print data_list
            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Between Hour Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)



class CreateView(generic.View):

    def post(self, request, *args, **kwargs):
        data = Data()

        result = check_device(**request.POST)

        if result:
            try:
                device = Device.objects.get(device_mac=result["device_mac"])
            except Device.DoesNotExist:
                new_device = {}
                new_device["device_ip"] = result["device_ip"]
                new_device["device_mac"] = result["device_mac"]
                new_device["label"] = result["label"]
                try:
                    new_device['devicestate'] = DeviceState.objects.get(id=result['devicestate'])
                except Exception as e:
                    #TODO: create default devicestates in settings.py
                    new_device['devicestate'] = DeviceState.objects.get(name="off")

                try:
                    new_device['owner'] = User.objects.get(username=result['owner'])
                except Exception as e:
                    #TODO: create default user in settings.py
                    new_device['owner'] = User.objects.get(username="root")
                new_device["enabled"] = False
                print "NEW DEVICE:"
                print new_device
                device = Device(**new_device)
                device.save()

            device_enabled = device.enabled
            if device_enabled:
                result = check_data(**request.POST)
                if result:
                    data.data_value = result["data_value"]
                    data.device = device
                    data.date = datetime.datetime.now() #TODO: Device sends real datetime
                    data.save()

        return JsonResponse({'status':True})


class DataDatePostView(generic.DetailView):
    model = Data

    def post(self, request, *args, **kwargs):

        postdata = request.POST

        try:
            data_list = []

            if "hour" in postdata:
                hour = postdata["hour"]
            else:
                hour = "1"

            if "day" in postdata:
                day = postdata["day"]
            else:
                day = "1"

            if "month" in postdata:
                month = postdata["month"]
            else:
                month = "1"

            if "year" in postdata:
                year = postdata["year"]
            else:
                year = "1"

            if "device_id" in postdata:
                device_id = postdata["device_id"]
            else:
                device_id = ""

            if (day != "1"):
                if (hour != "1"):
                    datetime_string = day + "-" + month + "-" + year + " " + hour + ":" + "00"
                    #date = dp.parse(date_string, timezone.now())
                    date_from = datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M")
                    date_from = to_localtime(date_from) #TODO: Get timezone from country configured by user
                    date_to = date_from + timedelta(minutes=59)
                else:
                    date_string = day + "-" + month + "-" + year
                    date_from = datetime.datetime.strptime(date_string, "%d-%m-%Y").date()
                    date_from = to_localtime(date_from) #TODO: Get timezone from country configured by user
                    date_to = date_from + timedelta(hours=24)
            elif (month != "1"):
                day = "1"
                cant_days_month = monthrange(int(year), int(month))[1]

                date_string = day + "-" + month + "-" + year
                #date = dp.parse(date_string, timezone.now())
                date_from = datetime.datetime.strptime(date_string, "%d-%m-%Y").date()
                date_to = date_from + timedelta(days=cant_days_month)
            else:
                day = "1"
                month = "1"
                year = "1" #TODO: timedelta de todo el año

            if (device_id):
                if (year == "1") and (month == "1") and (day == "1"):
                    data_query = Data.objects.all().filter(device=device_id)
                else:
                    data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to, device=device_id)
            else:
                if (year == "1") and (month == "1") and (day == "1"):
                    data_query = Data.objects.all()
                else:
                    data_query = Data.objects.all().filter(date__gte=date_from, date__lte=date_to)

            data_query = list(data_query)
            print len(data_query)
            for data in data_query:
                data_list.insert(0,data.serialize())

            return JsonResponse({'data': data_list})

        except Exception as e:
            print "Some error ocurred getting Day Data"
            print "Exception: " + str(e)
            return HttpResponse(status=500)
