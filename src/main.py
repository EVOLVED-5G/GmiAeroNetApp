import os
import json

from header_file import *
from auth import ask_access_token
from sdk_location_tools import *
from sdk_QoS_tools import *

from fastapi import FastAPI, Request
#from pydantic import BaseModel
from fastapi.responses import HTMLResponse

#class Document(BaseModel):
 #   words: str

app = FastAPI()

objLoc = location_sub()
objQos = qos_sub()

# Call me only when working locally for dev/debug
def add_local_env_var():
    print("local vars")
    os.environ['NETAPP_NAME'] = "GMI_Netapp"
    os.environ['NETAPP_ID'] = "gmi_netapp"
    os.environ['NETAPP_IP'] = "http://127.0.0.1:"
    os.environ['NETAPP_SERVER_VAPP'] = "127.0.0.1"
    os.environ['NETAPP_PORT_5G'] = ""
    os.environ['NETAPP_PORT_WEB'] = ""
    os.environ['NETAPP_PORT_VAPP'] = "8000"
    os.environ['NEF_HOST'] = "http://localhost:8888"
    os.environ['NEF_CALLBACK_URL'] = "http://host.docker.internal:"

@app.on_event("startup")
async def startup_event():
    add_local_env_var()
    print_initmess()

@app.get('/', response_class=HTMLResponse)
async def root():
   return return_defaultMess()

@app.get('/sdk_location/{externalId}')
async def root(externalId: str):
   external_id = externalId #"10002@domain.com"
   response = create_single_request_for_location_info(external_id)
   return response

@app.get('/sdk_location_delete_sub')
async def root():
   response = read_and_delete_all_existing_loc_subscriptions()
   print(response)
   return response

@app.get('/sdk_location_create_sub/{externalId}')
async def root(externalId: str):
   external_id = externalId #"10002@domain.com"
   response = create_subscription_and_retrieve_call_backs(external_id)
   print(response)
   return response

@app.post("/monitoring/callback")   #location callback
async def create_item(req: Request):
    document_json = await req.json()
    objLoc.subName = document_json['subscription']
    objLoc.extID = document_json['externalId']
    objLoc.cellID = document_json['locationInfo']['cellId']
    jsonStr = json.dumps(objLoc.__dict__)
    print(jsonStr)
    print(document_json)
    return document_json

@app.get('/get_last_locInfo')
async def root():
    jsonStr = json.dumps(objLoc.__dict__)
    #print(jsonStr)
    return jsonStr

@app.get('/sdk_qos_delete_sub')
async def root():
   response = read_and_delete_all_existing_qos_subscriptions()
   print(response)
   return response

@app.get('/sdk_qos_create_sub')
async def root():
   response = create_non_quaranteed_bit_rate_subscription_for_live_streaming()
   print(response)
   return response

@app.post("/monitoring/qos_callback")   #location callback
async def create_item(req: Request):
    document_json = await req.json()
    objQos.transaction = document_json['transaction']
    objQos.ipv4addr = document_json['ipv4Addr']
    objQos.event = document_json['eventReports'][0]['event']
    jsonStr = json.dumps(objLoc.__dict__)
    print(jsonStr)
    print(document_json)
    return document_json

@app.get('/get_last_qosInfo')
async def root():
    jsonStr = json.dumps(objQos.__dict__)
    #print(jsonStr)
    return jsonStr
