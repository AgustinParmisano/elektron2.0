"""elektron URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from devices import views as device_views
from data import views as data_views
from tasks import views as task_views
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'devices', device_views.DeviceViewSet)
router.register(r'devicestates', device_views.DeviceStateViewSet)
router.register(r'users', device_views.UserViewSet)
router.register(r'data', data_views.DataViewSet)
#router.register(r'tasks', task_views.TaskViewSet)
router.register(r'datetimetasks', task_views.DateTimeTaskViewSet)
router.register(r'datatasks', task_views.DataTaskViewSet)
router.register(r'taskstates', task_views.TaskStateViewSet)
router.register(r'taskfunction', task_views.TaskFunctionViewSet)


schema_view = get_schema_view(title='Pastebin API')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^schema/$', schema_view),
]
