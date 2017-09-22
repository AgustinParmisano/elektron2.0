from rest_framework import serializers
from tasks.models import Task, DateTimeTask, DataTask, TaskState, TaskFunction
from devices.models import Device
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    owner = Device.owner

class DateTimeTaskSerializer(TaskSerializer):
    datetimetask_detail = serializers.HyperlinkedIdentityField(view_name='datetimetask-detail', format='html')
    device_detail = serializers.HyperlinkedIdentityField(view_name='datetimetask-device', format='html')

    class Meta:
        model = DateTimeTask
        fields = ('id',  'label', 'datetimetask_detail', 'created', 'device', 'device_detail', 'date_from', 'date_to' ,'taskstate',  'owner', 'taskfunction')

class DataTaskSerializer(TaskSerializer):
    datatask_detail = serializers.HyperlinkedIdentityField(view_name='datatask-detail', format='html')
    device_detail = serializers.HyperlinkedIdentityField(view_name='datatask-device', format='html')

    class Meta:
        model = DataTask
        fields = ('id',  'label', 'datatask_detail', 'created', 'device', 'device_detail', 'data_value' ,'taskstate',  'owner', 'taskfunction')


class DeviceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #highlight = serializers.HyperlinkedIdentityField(view_name='device-highlight', format='html')
    data = serializers.HyperlinkedIdentityField(view_name='device-data', format='html')

    class Meta:
        model = Device
        fields = ('id', 'device_ip', 'device_mac', 'created', 'label', 'devicestate', 'owner', 'data')

class TaskStateSerializer(serializers.ModelSerializer):
    task_state_detail = serializers.HyperlinkedIdentityField(view_name='taskstate-detail', format='html')
    task = serializers.HyperlinkedIdentityField(view_name='taskstate-task', format='html')

    class Meta:
        model = TaskState
        fields = ('id', 'name', 'description', 'task', 'task_state_detail')

class TaskFunctionSerializer(serializers.ModelSerializer):
    task_function_detail = serializers.HyperlinkedIdentityField(view_name='taskfunction-detail', format='html')
    task = serializers.HyperlinkedIdentityField(view_name='taskfunction-task', format='html')

    class Meta:
        model = TaskFunction
        fields = ('id', 'name', 'description', 'task', 'task_function_detail')


class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'tasks')
