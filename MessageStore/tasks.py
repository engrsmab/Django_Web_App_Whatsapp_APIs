from celery import Celery, shared_task
from .models import Device, Client, Data
from .helper import general_state
import requests
import os

TOKEN = os.environ.get('TOKEN')


@shared_task()
def notification_telegram():
    try:
        devices = Device.objects.all()
        for device in devices:
            clients = device.clients.all()
            try:
                data = device.data_set.all()[0]
                for client in clients:
                    result = general_state(data, client.language)
                    x = requests.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode=HTML'.format(
                        TOKEN, client.chat_id, result))
            except:
                pass
    except:
        return

@shared_task()
def log():
    print('test')