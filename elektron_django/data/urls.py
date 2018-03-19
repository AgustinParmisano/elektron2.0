from django.conf.urls import url

from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'data'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^perhour$', views.DataPerHourView.as_view(), name='perhour'),
    url(r'^perday$', views.DataPerDayView.as_view(), name='perday'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^create$', csrf_exempt(views.CreateView.as_view()), name='create'),
    url(r'^(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/$', csrf_exempt(views.DataDayView.as_view()), name='data_day'),
    url(r'^(?P<month>\d{2})/(?P<year>\d{4})/$', csrf_exempt(views.DataMonthView.as_view()), name='data_month'),
    url(r'^(?P<day1>\d{2})/(?P<month1>\d{2})/(?P<year1>\d{4})/(?P<day2>\d{2})/(?P<month2>\d{2})/(?P<year2>\d{4})/$', csrf_exempt(views.DataBetweenDaysView.as_view()), name='data_between_days'),
    url(r'^(?P<day1>\d{2})/(?P<month1>\d{2})/(?P<year1>\d{4})/(?P<day2>\d{2})/(?P<month2>\d{2})/(?P<year2>\d{4})/perhour$', csrf_exempt(views.DataBetweenDaysPerhourView.as_view()), name='data_between_days_perhour'),
    url(r'^(?P<day1>\d{2})/(?P<month1>\d{2})/(?P<year1>\d{4})/(?P<day2>\d{2})/(?P<month2>\d{2})/(?P<year2>\d{4})/perday$', csrf_exempt(views.DataBetweenDaysPerdayView.as_view()), name='data_between_days_perday'),
    url(r'^(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/(?P<hour>\d{2})/$', csrf_exempt(views.DataHourView.as_view()), name='data_hour'),
    url(r'^(?P<day1>\d{2})/(?P<month1>\d{2})/(?P<year1>\d{4})/(?P<hour1>\d{2})/(?P<day2>\d{2})/(?P<month2>\d{2})/(?P<year2>\d{4})/(?P<hour2>\d{2})/$', csrf_exempt(views.DataBetweenHoursView.as_view()), name='data_between_hours'),
    url(r'^(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/perhour$', csrf_exempt(views.DataDayPerHourView.as_view()), name='data_day_perhour'),
    url(r'^(?P<month>\d{2})/(?P<year>\d{4})/perhour$', csrf_exempt(views.DataMonthPerHourView.as_view()), name='data_month_perhour'),
    url(r'^date$', csrf_exempt(views.DataDatePostView.as_view()), name='data_date_post'),
    url(r'^days$', csrf_exempt(views.DataBetweenDaysPostView.as_view()), name='data_days_post'),
    url(r'^hours$', csrf_exempt(views.DataBetweenHoursPostView.as_view()), name='data_hours_post'),
    url(r'^offsetlimit/(?P<offset>\d+)/(?P<limit>\d+)/(?P<order>\d+)/$', csrf_exempt(views.GetDataOffsetLimit.as_view()), name='get_data_offset_limit'),
    url(r'^totaldata$', csrf_exempt(views.GetTotalData.as_view()), name='get_total_data'),
    url(r'^totalwattstaxco2$', csrf_exempt(views.GetDataWattsTaxCo2.as_view()), name='get_total_watts_tax_co2'),
]
