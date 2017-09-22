# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from data.models import Data
from devices.models import Device
from data.serializers import DataSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from data.permissions import IsOwnerOrReadOnly, IsDataOrNothing
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.renderers import JSONRenderer as renderers
from rest_framework import renderers
from rest_framework.parsers import JSONParser
import json
import datetime

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'data': reverse('data-list', request=request, format=format)
    })


class DataViewSet(viewsets.ModelViewSet):
    #lookup_field = "data_value"
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    """

    permission_classes = (IsDataOrNothing,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer, renderers.JSONRenderer])
    def device(self, request, *args, **kwargs):
        queryset = Device.objects.all()
        data = self.request.query_params.get('data', self.get_object())

        if data is not None:
            device = queryset.filter(data=data)[0]

        device_json = device.__dict__
        device_json['created'] = device_json['created']

        return Response(json.dumps(device_json, default = myconverter))

    def perform_create(self, serializer):
        serializer.save()
