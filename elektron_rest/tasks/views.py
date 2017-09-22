# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tasks.models import Task, DateTimeTask, DataTask, TaskState, TaskFunction
from devices.models import Device
from tasks.serializers import TaskSerializer, DateTimeTaskSerializer, DataTaskSerializer, TaskStateSerializer, TaskFunctionSerializer, DeviceSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from tasks.permissions import IsOwnerOrReadOnly, IsTaskOrNothing, IsTaskStateOrNothing, IsTaskFunctionOrNothing
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework import renderers
import json
import datetime
from rest_framework.parsers import JSONParser

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'tasks': reverse('task-list', request=request, format=format)
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

"""
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    #permission_classes = (IsTaskOrNothing,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer, renderers.JSONRenderer])
    def device(self, request, *args, **kwargs):
        queryset = Device.objects.all()
        task = self.request.query_params.get('task', self.get_object())

        if task is not None:
            device = queryset.filter(task=task)[0]

        device_json = device.__dict__
        device_json['created'] = device_json['created']

        return Response(json.dumps(device_json, default = myconverter))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
"""

class DateTimeTaskViewSet(viewsets.ModelViewSet):
    queryset = DateTimeTask.objects.all()
    serializer_class = DateTimeTaskSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    #permission_classes = (IsTaskOrNothing,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer, renderers.JSONRenderer])
    def device(self, request, *args, **kwargs):
        queryset = Device.objects.all()
        datetimetask = self.request.query_params.get('datetimetask', self.get_object())

        if datetimetask is not None:
            device = queryset.filter(task=datetimetask)[0]

        device_json = device.__dict__
        device_json['created'] = device_json['created']

        return Response(json.dumps(device_json, default = myconverter))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DataTaskViewSet(viewsets.ModelViewSet):
    queryset = DataTask.objects.all()
    serializer_class = DataTaskSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    #permission_classes = (IsTaskOrNothing,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer, renderers.JSONRenderer])
    def device(self, request, *args, **kwargs):
        queryset = Device.objects.all()
        datatask = self.request.query_params.get('datatask', self.get_object())

        if datatask is not None:
            device = queryset.filter(task=datatask)[0]

        device_json = device.__dict__
        device_json['created'] = device_json['created']

        return Response(json.dumps(device_json, default = myconverter))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskStateViewSet(viewsets.ModelViewSet):
    queryset = TaskState.objects.all()
    serializer_class = TaskStateSerializer

    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)

    permission_classes = (IsTaskStateOrNothing,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer, renderers.JSONRenderer])
    def task(self, request, *args, **kwargs):
        queryset = Task.objects.all()
        taskstate = self.request.query_params.get('taskstate ', self.get_object())

        if taskstate is not None:
            task_list_query = queryset.filter(taskstate=taskstate )

        task_list = []

        for task in task_list_query:
            task_json = task.__dict__
            #task_json['date'] = task_json['date']
            task_list.append(task_json)

        return Response(json.dumps(task_list, default = myconverter))

    def perform_create(self, serializer):
        serializer.save()

class TaskFunctionViewSet(viewsets.ModelViewSet):
    queryset = TaskFunction.objects.all()
    serializer_class = TaskFunctionSerializer

    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                      IsOwnerOrReadOnly,)

    permission_classes = (IsTaskFunctionOrNothing,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer, renderers.JSONRenderer])
    def task(self, request, *args, **kwargs):
        queryset = Task.objects.all()
        taskfunction = self.request.query_params.get('taskfunction ', self.get_object())

        if taskfunction is not None:
            task_list_query = queryset.filter(taskfunction=taskfunction )

        task_function_list = []

        for task in task_list_query:
            task_json = task.__dict__
            #task_json['date'] = task_json['date']
            task_function_list.append(task_json)

        return Response(json.dumps(task_function_list, default = myconverter))

    def perform_create(self, serializer):
        serializer.save()
