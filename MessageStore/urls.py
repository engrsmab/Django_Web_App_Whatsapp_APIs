from django.urls import path
from .views import message_handle, getDataDevice, getGroup, getDevice, message_handle_v1
urlpatterns = [
    path('<str:imei>/', message_handle, name='message'),
    path('v1/<str:imei>/', message_handle_v1, name='message'),
    path('group/<str:user_id>/', getGroup, name="getGroup"),
    path('data/<str:device_imei>/', getDataDevice, name='getDataDevice'),
    path('devices/<str:group_name>/', getDevice, name='getDeviceGroup'),
]
