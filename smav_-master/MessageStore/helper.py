from datetime import datetime
from .models import Device, Client, Data, DeviceGroup, Language
from webhooks.helper import send_whatsapp
import json
from asgiref.sync import sync_to_async
import requests
import os

TOKEN = os.environ.get('TOKEN')


def send_telegram(_case, chat_id, lang, device, item):
    try:
        language = Language.objects.get(name=lang)
        match _case:
            case 'gas':
                x = requests.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode=HTML'.format(
                    TOKEN, chat_id, '<b>{0} ({2})</b>\r\n{1} {3}%'.format(device.name, language.gasWarning, device.phone, item.gas)))
            case 'vol':
                x = requests.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode=HTML'.format(
                    TOKEN, chat_id, '<b>{0} ({2})</b>\r\n{1}'.format(device.name, language.volWarning, device.phone)))
            case 't1':
                x = requests.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode=HTML'.format(
                    TOKEN, chat_id, '<b>{0} ({2})</b>\r\n{1} {3}°C'.format(device.name, language.tempWarning, device.phone, item.temperature1)))
            case 't2':
                x = requests.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode=HTML'.format(
                    TOKEN, chat_id, '<b>{0} ({2})</b>\r\n{1}'.format(device.name, language.inverWarning, device.phone)))
            case 'start':
                x = requests.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode=HTML'.format(
                    TOKEN, chat_id, '<b>{0} ({2})</b>\r\n{1}'.format(device.name, language.machineStart, device.phone)))
            case 'stop':
                x = requests.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode=HTML'.format(
                    TOKEN, chat_id, '<b>{0} ({2})</b>\r\n{1}'.format(device.name, language.machineStop, device.phone)))
            case 'machine_not_start':
                x = requests.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode=HTML'.format(
                    TOKEN, chat_id, '<b>{0} ({2})</b>\r\n{1}'.format(device.name, language.machineWarning, device.phone)))
            case 'machine_error':
                x = requests.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode=HTML'.format(
                    TOKEN, chat_id, '<b>{0} ({2})</b>\r\n{1}'.format(device.name, language.machineErorr, device.phone)))

    except:
        return
    pass


def find_device(imei):
    try:
        device = Device.objects.get(imei=imei)
        return device
    except:
        return []
        

def save_data_v1(body, device):
    items = Data.objects.filter(device=device)
    items.delete()
    try:
        data = json.loads(body)
        item = Data.objects.create(temperature1=data['T1'], humidity1=data['H1'], temperature2=data['T2'],
                                   humidity2=data['H2'],
                                   wind=data['wind'], gas=data['gas'], voltage=float(data['voltage']), machineStatus=float(data['machine']), mode = float(data['mode']), signal = float(data['signal']), volBat = float(data['vbat']), temperatureH1 = float(data['TH1']),temperatureH2 = float(data['TH2']), device=device)
        item.save()
        device.active = 2
        device.save()
        if(device.timeStart.day - datetime.now().day < 0):
            device.timeActive = 0
            device.save()
        if float(data['machine']) >= 12:
            delta = item.datetime - device.timeStart
            _timeActive = float(device.timeActive) + delta.total_seconds()
            if(_timeActive > 5*60):
                device.timeStart = datetime.now()
            else:
                device.timeActive = _timeActive
                device.timeStart = datetime.now()
            device.save()
        clients = device.clients.all()
        for client in clients:
            if int(client.alertStatus) == 1:
                if float(data['voltage']) < 11:
                    send_telegram('vol', client.chat_id,
                                  client.language, device, item)
                if int(data['T1']) <= int(client.temperatureAlert):
                    send_telegram('t1', client.chat_id,
                                  client.language, device, item)
                if (int(data['T2']) - int(data['T1'])) < 1:
                    send_telegram('t2', client.chat_id,
                                  client.language, device, item)
                if int(data['gas']) <= 49:
                    send_telegram('gas', client.chat_id,
                                  client.language, device, item)
                if float(data['machine']) >= client.machineVoltage and client.lastmessage == 0:
                    send_telegram('start', client.chat_id,
                                  client.language, device, item)
                    client.lastmessage = 1
                    client.save()
                if float(data['machine']) < client.machineVoltage and client.lastmessage == 1:
                    send_telegram('stop', client.chat_id,
                                  client.language, device, item)
                    client.lastmessage = 0
                    client.save()
                if int(data['T1']) < client.temperatureAlert and float(data['machine']) < client.machineVoltage and client.lastmessage == 1:
                    send_telegram('machine_not_start',
                                  client.chat_id, client.language, device, item)
                if int(data['T1']) < client.temperatureAlert and float(data['machine']) < client.machineVoltage and client.lastmessage == 0:
                    send_telegram('machine_error',
                                  client.chat_id, client.language, device, item)
        return 0
    except:
        return 1

def save_data(body, device):
    items = Data.objects.filter(device=device)
    items.delete()
    try:
        data = json.loads(body)
        
        item = Data.objects.create(temperature1=data['T1'], humidity1=data['H1'], temperature2=data['T2'],
                                   humidity2=data['H2'],
                                   wind=data['wind'], gas=data['gas'], voltage=float(data['voltage']), machineStatus=float(data['machine']), device=device)
        item.save()
        if(device.timeStart.day - datetime.now().day < 0):
            device.timeActive = 0
            device.save()
        if float(data['machine']) >= 12:
            delta = item.datetime - device.timeStart
            _timeActive = float(device.timeActive) + delta.total_seconds()
            if(_timeActive > 5*60):
                device.timeStart = datetime.now()
            else:
                device.timeActive = _timeActive
                device.timeStart = datetime.now()
            device.save()
        clients = device.clients.all()
        for client in clients:
            if int(client.alertStatus) == 1:
                if float(data['voltage']) < 11:
                    send_telegram('vol', client.chat_id,
                                  client.language, device, item)
                if int(data['T1']) <= int(client.temperatureAlert):
                    send_telegram('t1', client.chat_id,
                                  client.language, device, item)
                if (int(data['T2']) - int(data['T1'])) < 1:
                    send_telegram('t2', client.chat_id,
                                  client.language, device, item)
                if int(data['gas']) <= 49:
                    send_telegram('gas', client.chat_id,
                                  client.language, device, item)
                if float(data['machine']) >= client.machineVoltage and client.lastmessage == 0:
                    send_telegram('start', client.chat_id,
                                  client.language, device, item)
                    client.lastmessage = 1
                    client.save()
                if float(data['machine']) < client.machineVoltage and client.lastmessage == 1:
                    send_telegram('stop', client.chat_id,
                                  client.language, device, item)
                    client.lastmessage = 0
                    client.save()
                if int(data['T1']) < client.temperatureAlert and float(data['machine']) < client.machineVoltage and client.lastmessage == 1:
                    send_telegram('machine_not_start',
                                  client.chat_id, client.language, device, item)
                if int(data['T1']) < client.temperatureAlert and float(data['machine']) < client.machineVoltage and client.lastmessage == 0:
                    send_telegram('machine_error',
                                  client.chat_id, client.language, device, item)
        return 1
    except:
        return 1

def general_state(item, name):

    try:
        lang = Language.objects.get(name=name)
        if float(item.machineStatus) < 12:
            machine = "OFF"
        else:
            machine = "ON"
        result = '<b>{0} ({18})</b>\r\n{9}: {1}°C \r\n{10}: {2}% RH\r\n{11}: {3}°C  \r\n{12}: {4}% RH\r\n{13}: {5}  Km/hr\r\n{14}: {6}%\r\n{15}: {7}\r\n{16}:{8}V\r\n<i>{17}</i>"\r\n'.format(
            item.device.name, item.temperature1, item.humidity1, item.temperature2, item.humidity2, item.wind, item.gas, machine, item.voltage, lang.temperature1, lang.humidity1, lang.temperature2, lang.humidity2, lang.wind, lang.gas, lang.machineStatus, lang.voltage, '{0} GMT+0'.format(item.datetime), item.device.phone)
        return result
    except:
        return 'Not Found'


def temperature(item, name):
    try:
        lang = Language.objects.get(name=name)
        result = '<b>{0} ({10})</b>\r\n{5}: {1}°C \r\n{6}: {2}% RH\r\n{7}: {3}°C\r\n{8}: {4}% RH\r\n<i>{9}</i>"\r\n'.format(
            item.device.name, item.temperature1, item.humidity1, item.temperature2, item.humidity2, lang.temperature1, lang.humidity1, lang.temperature2, lang.humidity2, '{0} GMT+0'.format(item.datetime), item.device.phone)
        return result
    except:
        return 'Not Found'


def wind(item, name):
    try:
        lang = Language.objects.get(name=name)
        result = '<b>{0} ({4})</b>\r\n{2}: {1} Km/hr\r\n <i>{3}</i>"\r\n'.format(
            item.device.name, item.wind, lang.wind, '{0} GMT+0'.format(item.datetime), item.device.phone)
        return result
    except:
        return 'Not Found'


def gas(item, name):
    try:
        lang = Language.objects.get(name=name)
        result = '<b>{0} ({4})</b>\r\n{2}: {1}%\r\n<i>{3}</i>"\r\n'.format(
            item.device.name, item.gas, lang.gas, '{0} GMT+0'.format(item.datetime), item.device.phone)
        return result
    except:
        return 'Not Found'


def machine_state(item, name):
    try:
        lang = Language.objects.get(name=name)
        if float(item.machineStatus) < 12:
            machine = "OFF"
        else:
            machine = "ON"
        result = '<b>{0} ({4})</b>\r\n{2} {1}\r\n<i>{3}</i>"\r\n'.format(
            item.device.name, machine, lang.machineStatus, '{0} GMT+0'.format(item.datetime), item.device.phone)
        return result
    except:
        return 'Not Found'


def _get_data(chat_id, imei, query_type):
    try:
        client = Client.objects.get(chat_id=chat_id)
        device = Device.objects.get(imei=imei)
        try:
            item = device.data_set.latest('datetime')
        except:
            return 'No Data From Device'
        match query_type.lower():
            case '1':
                return general_state(item, client.language)
            case '2':
                return temperature(item, client.language)
            case '3':
                return wind(item, client.language)
            case '4':
                return gas(item, client.language)
            case '5':
                return machine_state(item, client.language)
    except:
        return 'No Device available'

def getData(imei):
    try:
        device = Device.objects.get(imei=imei)
        item = device.data_set.latest('datetime')
        return [item]
    except:
        return []

def _set_language(chat_id, language):
    try:
        item = Language.objects.get(name=language)
    except:
        return 'input false'
    client = Client.objects.get(chat_id=chat_id)
    client.language = language
    client.save()


def _language():
    data = []
    try:
        items = Language.objects.all()
        for item in items:
            data.append(item.name)
        return data
    except:
        return []


def _get_device(pk):
    result = []
    try:
        group = DeviceGroup.objects.get(id=pk)
        devices = group.devices.all()
        for device in devices:
            result.append([device.name, device.phone, device.imei])
        return result
    except:
        return []

def getAllDevice(name):
    try:
        group = DeviceGroup.objects.filter(name=name).get()
        print(group)
        devices = group.devices.all()
        return devices
    except:
        return []


def _get_group(chat_id):
    result = []
    try:
        client = Client.objects.get(chat_id=chat_id)
        groups = client.devicegroup_set.all()
        for group in groups:
            result.append([group.name, group.description, group.id])
        return result
    except:
        return []

def getUserGroup(chat_id):
    try:
        client = Client.objects.get(chat_id=chat_id)
        groups = client.devicegroup_set.all().defer("whatsapps")
        return groups
    except:
        return []

def _keyboard(chat_id):
    try:
        client = Client.objects.get(chat_id=chat_id)
        lang = Language.objects.get(name=client.language)
        reply_keyboard = [
            [lang.device, lang.type],
            [lang.language, lang.get_id],
            ["Done"],
        ]
        return reply_keyboard
    except:
        []


def _set_alarm(chat_id, value):
    try:
        client = Client.objects.get(chat_id=chat_id)
        client.alertStatus = value
        client.save()
    except:
        return


get_data = sync_to_async(_get_data, thread_sensitive=True)
set_language = sync_to_async(_set_language, thread_sensitive=True)
language = sync_to_async(_language, thread_sensitive=True)
get_device = sync_to_async(_get_device, thread_sensitive=True)
keyboard = sync_to_async(_keyboard, thread_sensitive=True)
set_alarm = sync_to_async(_set_alarm, thread_sensitive=True)
get_group = sync_to_async(_get_group, thread_sensitive=True)
