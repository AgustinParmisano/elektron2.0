from rest_framework import serializers
from devices.models import Device, DeviceState
from data.models import Data
from django.contrib.auth.models import User

class DeviceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    device_detail = serializers.HyperlinkedIdentityField(view_name='device-detail', format='html')
    data = serializers.HyperlinkedIdentityField(view_name='device-data', format='html')
    device_state_detail = serializers.HyperlinkedIdentityField(view_name='devicestate-detail', format='html')

    class Meta:
        model = Device
        fields = ('id', 'device_detail', 'device_ip', 'device_mac', 'created', 'label', 'devicestate', 'device_state_detail', 'owner', 'data')

class DeviceStateSerializer(serializers.ModelSerializer):
    device_state_detail = serializers.HyperlinkedIdentityField(view_name='devicestate-detail', format='html')
    device = serializers.HyperlinkedIdentityField(view_name='devicestate-device', format='html')

    class Meta:
        model = DeviceState
        fields = ('id', 'name', 'device_state_detail', 'description', 'device')


class UserSerializer(serializers.ModelSerializer):
    devices = serializers.PrimaryKeyRelatedField(many=True, queryset=Device.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'devices')
