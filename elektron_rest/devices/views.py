# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from devices.models import Device, DeviceState
from data.models import Data
from devices.serializers import DeviceSerializer, DeviceStateSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from devices.permissions import IsOwnerOrReadOnly, IsDeviceOrNothing, IsDeviceStateOrNothing
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework import renderers
import json
import datetime
from tornado_websockets.websocket import WebSocket
import pprint

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'devices': reverse('device-list', request=request, format=format)
    })


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    #lookup_field = "device_ip"
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)


    #permission_classes = (IsDeviceOrNothing,)


    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer, renderers.JSONRenderer])
    def data(self, request, *args, **kwargs):
        queryset = Data.objects.all()
        device = self.request.query_params.get('device', self.get_object())
        print device

        if device is not None:
            data_list_query = queryset.filter(device=device)

        data_list = []

        for data in data_list_query:
            data_json = data.__dict__
            data_json['date'] = data_json['date']
            data_list.append(data_json)

        return Response(json.dumps(data_list, default = myconverter))

    def perform_create(self, serializer):
        #print "REQUEST:"
        #pprint.pprint(self.request.user, width=1)

        try:
            username = self.request.user
            owner = User.objects.get(username=username)
        except Exception as e:
            owner = User.objects.get(username="device")
        #owner = User.objects.get(username=username)
        serializer.save(owner=owner)#self.request.user)


class DeviceStateViewSet(viewsets.ModelViewSet):
    #lookup_field = "device_ip"
    queryset = DeviceState.objects.all()
    serializer_class = DeviceStateSerializer

    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)

    permission_classes = (IsDeviceStateOrNothing,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer, renderers.JSONRenderer])
    def device(self, request, *args, **kwargs):
        queryset = Device.objects.all()
        devicestate = self.request.query_params.get('devicestate', self.get_object())

        if devicestate is not None:
            device_list_query = queryset.filter(devicestate=devicestate)

        device_list = []

        for device in device_list_query:
            device_json = device.__dict__
            #device_json['date'] = device_json['date']
            device_list.append(device_json)

        return Response(json.dumps(device_list, default = myconverter))


    def perform_create(self, serializer):
        serializer.save()
