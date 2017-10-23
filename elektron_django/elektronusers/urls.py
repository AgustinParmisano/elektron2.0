from django.conf.urls import url

from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'elektronusers'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', csrf_exempt(views.DetailView.as_view()), name='detail'),
    url(r'^login$', csrf_exempt(views.LoginView.as_view()), name='login'),
    url(r'^logout$', csrf_exempt(views.LogoutView.as_view()), name='logout'),
]