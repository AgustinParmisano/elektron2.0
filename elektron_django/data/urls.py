from django.conf.urls import url

from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'data'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^create$', csrf_exempt(views.CreateView.as_view()), name='create'),
    url(r'^(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/$', csrf_exempt(views.DataDayView.as_view()), name='data_day'),
    url(r'^(?P<month>\d{2})/(?P<year>\d{4})/$', csrf_exempt(views.DataMonthView.as_view()), name='data_month'),
    url(r'^(?P<day1>\d{2})/(?P<month1>\d{2})/(?P<year1>\d{4})/(?P<day2>\d{2})/(?P<month2>\d{2})/(?P<year2>\d{4})/$', csrf_exempt(views.DataBetweenDaysView.as_view()), name='data_between_days'),
    url(r'^(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/(?P<hour>\d{2})/$', csrf_exempt(views.DataHourView.as_view()), name='data_hour'),
    url(r'^(?P<day1>\d{2})/(?P<month1>\d{2})/(?P<year1>\d{4})/(?P<hour1>\d{2})/(?P<day2>\d{2})/(?P<month2>\d{2})/(?P<year2>\d{4})/(?P<hour2>\d{2})/$', csrf_exempt(views.DataBetweenHoursView.as_view()), name='data_between_hours'),
    url(r'^day$', csrf_exempt(views.DataDayPostView.as_view()), name='data_day_post'),
]
