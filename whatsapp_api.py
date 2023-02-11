import os,requests,json

Client_Token = "EAAGyZCKRC97sBAHI7Eiif59MH02Qq9EzACAULgQZBJeCAwKvmbVtYOUeB8Bb8BXvtZCd0s9LbwW1mxdcfIIIs1EDAHyXNYO3MZCPrGsnrt2D4Hwk7XTe9iZBOZATZBrzLFomJOD67AdCCKqtBxgdChfZBu18MDmZCdinU8coT0GynieLuCU1P8VnWCEWQzBfLm8lDRq7n27IB8prtuAQMfAoGS3rbppReqUQZD"
# client_app = "478273134065595"
client_phone = "0771101564"
client_phone_id = "102820472480059"



headers = {"Authorization": "OAuth {0}".format(Client_Token), "file_offset": "0"}
header2 = {"Authorization": "Bearer {0}".format(Client_Token), "Content-Type": "application/json"}
payload1 = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": client_phone,
    "type":"document",
   
    "document": json.dumps({
    "link": "https://github.com/attidev01/smav_/blob/master/webhooks/2023-02-05.pdf",
   
  })
}
resp = requests.post(f"https://graph.facebook.com/v15.0/{client_phone_id}/messages",headers=header2,data=payload1)
print(resp.json())







