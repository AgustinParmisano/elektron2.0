from django.conf.urls import url

from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'devices'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', csrf_exempt(views.DetailView.as_view()), name='detail'),
    url(r'^recognition$', csrf_exempt(views.RecognitionView.as_view()), name='recognition'),
    url(r'^create$', csrf_exempt(views.CreateView.as_view()), name='create'),
    url(r'^delete$', csrf_exempt(views.DeleteView.as_view()), name='delete'),
    url(r'^update$', csrf_exempt(views.UpdateView.as_view()), name='update'),
    url(r'^data$', csrf_exempt(views.DeviceMacDataView.as_view()), name='data_device_mac'),
    url(r'^(?P<pk>[0-9]+)/data/offsetlimit/(?P<offset>\d+)/(?P<limit>\d+)/(?P<order>\d+)/$', csrf_exempt(views.DeviceDataOffsetLimitView.as_view()), name='data_device_offset_limit'),
    url(r'^(?P<pk>[0-9]+)/totaldata$', csrf_exempt(views.DeviceTotalData.as_view()), name='get_total_data'),
    url(r'^task$', csrf_exempt(views.DeviceMacTaskView.as_view()), name='task_device_mac'),
    url(r'^(?P<pk>[0-9]+)/data$', csrf_exempt(views.DeviceDataView.as_view()), name='data'),
    url(r'^(?P<pk>[0-9]+)/tasks$', csrf_exempt(views.DeviceTaskView.as_view()), name='task'),
    url(r'^(?P<pk>[0-9]+)/data/(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/$', csrf_exempt(views.DeviceDataDayView.as_view()), name='device_data_day'),
    url(r'^(?P<pk>[0-9]+)/data/(?P<month>\d{2})/(?P<year>\d{4})/$', csrf_exempt(views.DeviceDataMonthView.as_view()), name='device_data_month'),
    url(r'^(?P<pk>[0-9]+)/data/(?P<day1>\d{2})/(?P<month1>\d{2})/(?P<year1>\d{4})/(?P<day2>\d{2})/(?P<month2>\d{2})/(?P<year2>\d{4})/$', csrf_exempt(views.DeviceDataBetweenDaysView.as_view()), name='device_data_between_days'),
    url(r'^(?P<pk>[0-9]+)/data/(?P<day1>\d{2})/(?P<month1>\d{2})/(?P<year1>\d{4})/(?P<day2>\d{2})/(?P<month2>\d{2})/(?P<year2>\d{4})/perhour$', csrf_exempt(views.DeviceDataBetweenDaysPerhourView.as_view()), name='device_data_between_days_perhour'),
    url(r'^(?P<pk>[0-9]+)/data/(?P<day1>\d{2})/(?P<month1>\d{2})/(?P<year1>\d{4})/(?P<day2>\d{2})/(?P<month2>\d{2})/(?P<year2>\d{4})/perday$', csrf_exempt(views.DeviceDataBetweenDaysPerdayView.as_view()), name='device_data_between_days_perday'),
    url(r'^(?P<pk>[0-9]+)/data/(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/(?P<hour>\d{2})/$', csrf_exempt(views.DeviceDataHourView.as_view()), name='device_data_hour'),
    url(r'^(?P<pk>[0-9]+)/data/(?P<day1>\d{2})/(?P<month1>\d{2})/(?P<year1>\d{4})/(?P<hour1>\d{2})/(?P<day2>\d{2})/(?P<month2>\d{2})/(?P<year2>\d{4})/(?P<hour2>\d{2})/$', csrf_exempt(views.DeviceDataBetweenHoursView.as_view()), name='device_data_between_hours'),
    url(r'^(?P<pk>[0-9]+)/lastdata/(?P<cant>\d+)/$', csrf_exempt(views.DeviceLastDataView.as_view()), name='device_lastdata'),
    url(r'^(?P<pk>[0-9]+)/data/(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/perhour$', csrf_exempt(views.DeviceDataDayPerHourView.as_view()), name='device_data_day_perhour'),
    url(r'^(?P<pk>[0-9]+)/data/(?P<month>\d{2})/(?P<year>\d{4})/perhour$', csrf_exempt(views.DeviceDataMonthPerHourView.as_view()), name='device_data_month_perhour'),
    url(r'^(?P<pk>[0-9]+)/data/(?P<month>\d{2})/(?P<year>\d{4})/perday$', csrf_exempt(views.DeviceDataMonthPerDayView.as_view()), name='device_data_month_perday'),
    url(r'^(?P<pk>[0-9]+)/data/perday$', csrf_exempt(views.DeviceDataPerDayView.as_view()), name='device_data_perday'),
    url(r'^(?P<pk>[0-9]+)/data/perhour$', csrf_exempt(views.DeviceDataPerHourView.as_view()), name='device_data_perhour'),
    url(r'^(?P<pk>[0-9]+)/shutdown$', csrf_exempt(views.ShutdownView.as_view()), name='shutdown'),
    url(r'^(?P<pk>[0-9]+)/turnon$', csrf_exempt(views.TurnonView.as_view()), name='turnon'),
    url(r'^(?P<pk>[0-9]+)/updatelabel$', csrf_exempt(views.UpdateLabelView.as_view()), name='updatelabel'),
    url(r'^(?P<pk>[0-9]+)/enable$', csrf_exempt(views.EnableView.as_view()), name='enable'),
    url(r'^(?P<pk>[0-9]+)/disable$', csrf_exempt(views.DisableView.as_view()), name='disable'),
    url(r'^(?P<pk>[0-9]+)/statistics$', csrf_exempt(views.DeviceStatisticsView.as_view()), name='statistics'),
    url(r'^statistics$', csrf_exempt(views.StatisticsView.as_view()), name='all_statistics'),
    url(r'^mac$', csrf_exempt(views.DeviceByMac.as_view()), name='get_device_by_mac'),
]
