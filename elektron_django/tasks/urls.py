from django.conf.urls import url

from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'tasks'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
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
]
