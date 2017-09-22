from rest_framework import serializers
from data.models import Data
from devices.models import Device
from django.contrib.auth.models import User

class DataSerializer(serializers.ModelSerializer):
    data_detail = serializers.HyperlinkedIdentityField(view_name='data-detail', format='html')
    device_detail = serializers.HyperlinkedIdentityField(view_name='data-device', format='html')

    class Meta:
        model = Data
        fields = ('id', 'data_detail','data_value', 'date', 'device', 'device_detail')

class DeviceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #highlight = serializers.HyperlinkedIdentityField(view_name='device-highlight', format='html')
    data = serializers.HyperlinkedIdentityField(view_name='device-data', format='html')

    class Meta:
        model = Device
        fields = ('id', 'device_ip', 'device_mac', 'created', 'label', 'state', 'owner', 'data')
