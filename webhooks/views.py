from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import re
from MessageStore.models import Device
import os,time
from threading import Thread
from .helper import get_reply_device, get_reply_type, reply_data, reply_text, set_language, set_alarm, get_reply_group, get_reply_setting
from .table_class import PDF_Generation
TOKEN_WHATSAPP = os.environ.get('TOKEN_WHATSAPP')
PHONE_ID = os.environ.get('PHONE_ID')

global global_data
global_data = None
# Create your views here.

headers = {"Authorization": "Bearer {0}".format(
    TOKEN_WHATSAPP), "Content-Type": "application/json"}
def create_pdf():
    global global_data
    if global_data != None:
        name = global_data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["description"] 
        device = Device.objects.get(imei=name)
        item = device.data_set.latest('datetime')
        pdf = PDF_Generation()
        pdf.get_pdf(item,device.name)
            
def save_pdf():
    while True:
        create_pdf()
        time.sleep(900)
pdf_thread = Thread(target=save_pdf)
pdf_thread.start()
def reply_whatsapp(payload):
    payload = json.dumps(payload)
    try:
        x = requests.post(
            f"https://graph.facebook.com/v13.0/{PHONE_ID}/messages", headers=headers, data=payload)
        print(x.content)
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=200)


@csrf_exempt
def hook_handle(request):
    global global_data
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        # Reply Menu
        try:
            if data["entry"] and data["entry"][0]["changes"] and data["entry"][0]["changes"][0] and data["entry"][0]["changes"][0]["value"]["messages"] and data["entry"][0]["changes"][0]["value"]["messages"][0]:
                checkMenu = re.search("^menu", data["entry"][0]["changes"][0]["value"]
                                  ["messages"][0]["text"]["body"], flags=re.IGNORECASE)
                checkSet = re.search("^set", data["entry"][0]["changes"][0]["value"]
                                  ["messages"][0]["text"]["body"], flags=re.IGNORECASE)
                if checkMenu:
                    data = get_reply_group(data["entry"][0]
                                           ["changes"][0]["value"]["contacts"][0]["wa_id"])
                    reply_whatsapp(data) 
                if checkSet:
                    data = get_reply_setting(data["entry"][0]
                                           ["changes"][0]["value"]["contacts"][0]["wa_id"])
                    reply_whatsapp(data)
        except:
            pass
        # case reply with result data from device after choose device and type  query
        try:
            if data["entry"] and data["entry"][0]["changes"] and data["entry"][0]["changes"][0] and data["entry"][0]["changes"][0]["value"]["messages"] and data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"] and data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"] and int(data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["id"]):
                description = data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["description"]
                check = re.search("^phone", description, flags=re.IGNORECASE)
                if check:
                    data = get_reply_type(data["entry"][0]
                                          ["changes"][0]["value"]["contacts"][0]["wa_id"], data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["id"])
                    for message in data:
                        reply_whatsapp(message)
                else:
                    global_data = data
                    data = reply_data(data["entry"][0]
                                      ["changes"][0]["value"]["contacts"][0]["wa_id"], data["entry"][0]["changes"][0]["value"]
                                      ["messages"][0]["interactive"]["list_reply"]["id"], data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["description"])
                    print(data)
                    reply_whatsapp(data)
        except:
            pass
        # case reply set language and reply type query
        try:
            if data["entry"] and data["entry"][0]["changes"] and data["entry"][0]["changes"][0] and data["entry"][0]["changes"][0]["value"]["messages"] and data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"] and data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]:
                name = data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["id"]
                check_lang = re.search("^language", name, flags=re.IGNORECASE)
                check_alarm = re.search("^alarm", name, flags=re.IGNORECASE)
                check_group = re.search("^group", name, flags=re.IGNORECASE)
                if check_lang:
                    set_language(data["entry"][0]
                                 ["changes"][0]["value"]["contacts"][0]["wa_id"], data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["title"])
                    data = reply_text(data["entry"][0]
                                      ["changes"][0]["value"]["contacts"][0]["wa_id"], "OK")
                    reply_whatsapp(data)
                elif check_alarm:
                    set_alarm(data["entry"][0]
                              ["changes"][0]["value"]["contacts"][0]["wa_id"], data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["title"])
                    data = reply_text(data["entry"][0]
                                      ["changes"][0]["value"]["contacts"][0]["wa_id"], "OK")
                    reply_whatsapp(data)
                elif check_group: #reply List device
                    data = get_reply_device(data["entry"][0]
                                            ["changes"][0]["value"]["contacts"][0]["wa_id"], data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["list_reply"]["title"])
                    for message in data:
                        print( message)
                        reply_whatsapp(message)
                    

        except:
            pass
        return HttpResponse(status=200)
    if request.method == 'GET':
        challenge = request.GET.get('hub.challenge')
        return HttpResponse(challenge, status=200)


def sms_handle(request):
    print(request.body)
    return HttpResponse('ok')
