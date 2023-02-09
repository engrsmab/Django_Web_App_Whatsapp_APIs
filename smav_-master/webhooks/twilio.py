import os
from twilio.rest import Client 
 
ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
MESS_SID= os.environ.get('MESS_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
 


def sms_service(phone, content):
    client = Client(ACCOUNT_SID, AUTH_TOKEN) 
    message = client.messages.create(  
                              messaging_service_sid= MESS_SID, 
                              body= content,      
                              to=phone 
                          ) 