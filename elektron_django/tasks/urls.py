from django.conf.urls import url

from . import views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

app_name = 'tasks'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^readytasks$', views.ReadyTasksView.as_view(), name='readytask_list'),
    url(r'^donetasks$', views.DoneTasksView.as_view(), name='donetask_list'),
    url(r'^readydatetimetasks$', views.ReadyDateTimeTasksView.as_view(), name='readydatetimetask_list'),
    url(r'^readydatatasks$', views.ReadyDataTasksView.as_view(), name='readydatatask_list'),
    url(r'^donedatetimetasks$', views.DoneDateTimeTasksView.as_view(), name='donedatetimetask_list'),
    url(r'^donedatatasks$', views.DoneDataTasksView.as_view(), name='donedatatask_list'),
    url(r'^datatasks$', views.DataTaskIndexView.as_view(), name='datatask_index'),
    url(r'^datetimetasks$', views.DateTimeTaskIndexView.as_view(), name='datatimetask_index'),
    url(r'^datatasks/(?P<pk>[0-9]+)/$', views.DataTaskDetailView.as_view(), name='datatask_detail'),
    url(r'^datetimetasks/(?P<pk>[0-9]+)/$', views.DateTimeTaskDetailView.as_view(), name='datatimetask_detail'),
    url(r'^datatasks/create$', csrf_exempt(views.DataTaskCreateView.as_view()), name='datatasks_create'),
    url(r'^datatasks/(?P<pk>[0-9]+)/update$', csrf_exempt(views.DataTaskUpdateView.as_view()), name='datatasks_update'),
    url(r'^devices/(?P<pk>[0-9]+)/datetimetasks$', csrf_exempt(views.DatetimeTaskDeviceView.as_view()), name='device_datetimetask'),
    url(r'^datetimetasks/create$', csrf_exempt(views.DateTimeTaskCreateView.as_view()), name='datetimetask_create'),
    url(r'^datetimetasks/(?P<pk>[0-9]+)/update$', csrf_exempt(views.DateTimeTaskUpdateView.as_view()), name='datetimetask_update'),
    url(r'^devices/(?P<pk>[0-9]+)/datatasks$', csrf_exempt(views.DataTaskDeviceView.as_view()), name='device_datatask'),
    url(r'^datetimetasks/(?P<pk>[0-9]+)/remove$', csrf_exempt(views.DateTimeTaskRemoveView.as_view()), name='remove_datetimetask'),
    url(r'^datatasks/(?P<pk>[0-9]+)/remove$', csrf_exempt(views.DataTaskRemoveView.as_view()), name='remove_datatask'),
    url(r'^taskstates$', views.TaskStatesView.as_view(), name='taskstates_list'),
    url(r'^taskfunctions$', views.TaskFunctionsView.as_view(), name='taskfunctions_list'),
    url(r'^datatasks/(?P<pk>[0-9]+)/updatestate$', csrf_exempt(views.DataTaskUpdateStateView.as_view()), name='datatasks_update_state'),
    url(r'^datetimetasks/(?P<pk>[0-9]+)/updatestate$', csrf_exempt(views.DateTimeTaskUpdateStateView.as_view()), name='datetimetasks_update_state'),
]
