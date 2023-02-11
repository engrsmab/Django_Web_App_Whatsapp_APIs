from django.urls import path
from .views import hook_handle, sms_handle

urlpatterns = [
    path('', hook_handle, name='hook'),
    path('sms/', sms_handle, name='sms')
]
