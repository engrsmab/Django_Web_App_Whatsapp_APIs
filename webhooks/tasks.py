from celery import shared_task
from MessageStore.models import Device, Data, Language
from webhooks.helper import send_whatsapp, whatsapp_send, general_state
from datetime import datetime, timezone
import os
from webhooks.twilio import sms_service

TOKEN = os.environ.get('TOKEN')


@shared_task()
def notification_whatsapp():
    try:
        devices = Device.objects.all()
        for device in devices:
            try:
                items = Data.objects.filter(device=device)
                item = items[0]
                whatsapps = device.whatsapps.all()
                for whatsapp in whatsapps:
                    if whatsapp.alertStatus == "ON" and device.active == 2:
                        if float(item.voltage) < 11:
                            send_whatsapp('vol', whatsapp.phone,
                                        whatsapp.language, device, item)
                        if int(item.temperature1) < int(whatsapp.temperatureAlert):
                            send_whatsapp('t1', whatsapp.phone,
                                        whatsapp.language, device, item)
                        if (int(item.temperature2) - int(item.temperature1)) < 1:
                            send_whatsapp('t2', whatsapp.phone,
                                        whatsapp.language, device, item)
                        if int(item.gas) <= 49:
                            send_whatsapp('gas', whatsapp.phone,
                                        whatsapp.language, device, item)
                        if float(item.machineStatus) >= whatsapp.machineVoltage and whatsapp.lastmessage == 0:
                            send_whatsapp('start', whatsapp.phone,
                                        whatsapp.language, device, item)
                            whatsapp.lastmessage = 1
                            whatsapp.save()
                        if float(item.machineStatus) < whatsapp.machineVoltage and whatsapp.lastmessage == 1:
                            send_whatsapp('stop', whatsapp.phone,
                                        whatsapp.language, device, item)
                            whatsapp.lastmessage = 0
                            whatsapp.save()
                        if int(item.temperature1) < whatsapp.temperatureAlert and float(item.machineStatus) < whatsapp.machineVoltage and whatsapp.lastmessage == 0:
                            send_whatsapp('machine_not_start', whatsapp.phone,
                                        whatsapp.language, device, item)
                        if int(item.temperature1) < whatsapp.temperatureAlert and float(item.machineStatus) < whatsapp.machineVoltage and whatsapp.lastmessage == 1:
                            send_whatsapp('machine_error', whatsapp.phone,
                                        whatsapp.language, device, item)
            except:
                pass
    except:
        return

@shared_task()
def notification_device_off():
    try:
        devices = Device.objects.all()
        for device in devices:
            whatsapps = device.whatsapps.all()
            try:
                items = Data.objects.filter(device=device)
                item = items[0]
                delta = datetime.now(timezone.utc) - item.datetime
                if delta.total_seconds() > 600 and device.active == 2:
                    print("ok")
                    for whatsapp in whatsapps:
                        language = Language.objects.get(name=whatsapp.language)
                        result = {"messaging_product": "whatsapp", "to": whatsapp.phone, "type": "text", "text": {"body": f"{language.nowDevice} {device.name}:({device.phone}) {language.offline}"}}
                        whatsapp_send(result)
                    device.active = 3
                    device.status = 0
                    device.save()
            except:
                if(device.active == 0):
                    for whatsapp in whatsapps:
                        language = Language.objects.get(name=whatsapp.language)
                        result = {"messaging_product": "whatsapp", "to": whatsapp.phone, "type": "text", "text": {"body": f"{language.nowDevice} {device.name}:({device.phone}) {language.offline}"}}
                        whatsapp_send(result) 
                    device.active = 3
                    device.status = 0
                    device.save()
                    pass
    except:
        return
            
@shared_task()
def notification_device_on():
    try:
        devices = Device.objects.all()
        for device in devices:
            whatsapps = device.whatsapps.all()
            try:
               if(device.status == 0 and device.active == 2): 
                    device.status = 1
                    device.save()
                    for whatsapp in whatsapps:
                        language = Language.objects.get(name=whatsapp.language)
                        result = {"messaging_product": "whatsapp", "to": whatsapp.phone, "type": "text", "text": {"body": f"{language.nowDevice} {device.name}:({device.phone}) {language.online}"}}
                        whatsapp_send(result)
            except:
                pass
    except:
        return
    
@shared_task()
def notification_sms():
    try:
        devices = Device.objects.all()
        for device in devices:
            try:
                items = Data.objects.filter(device=device)
                item = items[0]
                smsUsers = device.sms.all()
                for smsUser in smsUsers:
                    data = general_state(item, smsUser.language)
                    sms_service( smsUser.phone ,data)
            except:
                pass
    except:
        return
    
    
@shared_task()
def alertSMS():
    try:
        devices = Device.objects.all()
        for device in devices:
            try:
                items = Data.objects.filter(device=device)
                item = items[0]
                smsUsers = device.sms.all()
                for smsUser in smsUsers:
                    if smsUser.alertStatus == "ON" and device.active == 2:
                        language = Language.objects.get(name=smsUser.language)
                        if float(item.voltage) < 11:
                            data = '*{0} ({2})*\r\n{1} {3}v'.format(device.name, language.volWarning, device.phone, item.voltage)
                            sms_service( smsUser.phone ,data)
                        if int(item.temperature1) < int(smsUser.temperatureAlert):
                            data = '*{0} ({2})*\r\n{1} {3}°C'.format(device.name, language.tempWarning, device.phone, item.temperature1)
                            sms_service( smsUser.phone ,data)
                        if (int(item.temperature2) - int(item.temperature1)) < 1:
                            data = '*{0} ({2})*\r\n{1}'.format(device.name, language.inverWarning, device.phone)
                            sms_service( smsUser.phone ,data)
                        if int(item.gas) <= 49:
                           data = '*{0} ({2})*\r\n{1} {3}%'.format(device.name, language.gasWarning, device.phone, item.gas)
                           sms_service( smsUser.phone ,data)
                        if float(item.machineStatus) >= smsUser.machineVoltage and smsUser.lastmessage == 0:
                            data = '*{0} ({2})*\r\n{1}'.format(device.name, language.machineStart, device.phone)
                            sms_service( smsUser.phone ,data)
                            smsUser.lastmessage = 1
                            smsUser.save()
                        if float(item.machineStatus) < smsUser.machineVoltage and smsUser.lastmessage == 1:
                            data = '*{0} ({2})*\r\n{1}'.format(device.name, language.machineStop, device.phone)
                            sms_service( smsUser.phone ,data)
                            smsUser.lastmessage = 0
                            smsUser.save()
                        if int(item.temperature1) < smsUser.temperatureAlert and float(item.machineStatus) < smsUser.machineVoltage and smsUser.lastmessage == 0:
                            data = '*{0} ({2})*\r\n{1}'.format(device.name, language.machineWarning, device.phone)
                            sms_service( smsUser.phone ,data)
                        if int(item.temperature1) < smsUser.temperatureAlert and float(item.machineStatus) < smsUser.machineVoltage and smsUser.lastmessage == 1:
                            data = '*{0} ({2})*\r\n{1}'.format(device.name, language.machineErorr, device.phone)
                            sms_service( smsUser.phone ,data)
            except:
                pass
    except:
        return