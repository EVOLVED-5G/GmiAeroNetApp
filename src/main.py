import os
import sys

from fastapi import FastAPI, Body
from fastapi.responses import FileResponse, HTMLResponse

from header_file import *
from formatTools.str_tools import *
from formatTools.qos_info import *
from sdkTools.connectionMonitor_tools import *
from sdkTools.location_tools import *
from sdkTools.QoS_tools import *

#main declarations
app = FastAPI()
qoss = QOSINFO()

# This proc() is called only when working locally for dev/debug
def add_local_env_var():
    print("Set local vars : ...OK")
    os.environ['NETAPP_NAME'] = "GMI_Netapp"
    os.environ['NETAPP_ID'] = "gmi_netapp"
    os.environ['NETAPP_PORT_VAPP'] = "8383" 
    os.environ['NETAPP_PATH'] = ""
    os.environ['NEF_USER'] = "admin@my-email.com"
    os.environ['NEF_PASSWORD'] = "pass"    
    os.environ['NEF_ADDRESS'] = "http://localhost:8888"
    os.environ['NEF_CALLBACK_URL'] = "http://localhost:8383/monitoring/callback"
    os.environ['PATH_TO_CERTS'] = "..\..\config_files\certificates"
    os.environ['REQUESTED_UE_IP'] = "10.0.0.1"

# ALL RESPONSES CASES
@app.on_event("startup")
async def startup_event():
    #print("Argument List:", str(sys.argv))
    print_initmess()
    if(str(sys.argv).rfind("workers") > -1):  #if argument "workers" is passed, this is a local run, so call add_local_env_var()
        add_local_env_var()
    print("NETAPP_PATH : " + os.environ['NETAPP_PATH'])
    
""" DEFAULT RESPONSE """
@app.get('/', response_class=HTMLResponse)
async def root():
    #print(pathlib.Path().resolve())
    return FileResponse("." + os.environ['NETAPP_PATH'] + "/html/default.html")

""" RETURN CELL ID AFTER SENDING AN UE ID """
@app.get('/location_getCellID/{externalId}')
async def root(externalId: str):
   print("Emulator URL : " + Emulator_Utils.get_url_of_the_nef_emulator()) 
   response = location_getCellId(externalId)
   print("***********RESPONSE : " + str(response))
   returnStr = extractCellId(str(response))
   print("Cell ID for UE" , '\033[1m'  + externalId + '\033[0m',"requested : " + returnStr)
   return returnStr

""" RETURN CELL COORDONATES AFTER SENDING A UE ID """
@app.get('/location_getLatAndLong/{externalId}')
async def root(externalId: str): 
   response = location_getCellId(externalId)
   cellId = extractCellId(str(response))
   latAndLong = location_getLatAndLon(cellId)
   #print(str(latAndLong))
   returnStr = extractLatAndLong(str(latAndLong))
   print("Coordonates for UE ", '\033[1m'  + externalId + '\033[0m'," requested : " + returnStr)
   return returnStr 

""" CREATE BOTH CONNECTION SUBSCRIPTIONS """
@app.get('/connection_createSub', response_class=HTMLResponse)
async def root():
    response = connection_createSubscription()
    return response

""" DELETE ALL CONNECTION SUBSCRIPTIONS """
@app.get('/connection_deleteSub', response_class=HTMLResponse)
async def root():
    response = connection_deleteSubscription()
    return response

""" CREATE QOS QUARANTED SUBSCRIPTIONS """
@app.get('/qos_createQuarantedSubscription')
async def root():
    response = qos_createQuarantedSubscription()
    return response

""" CREATE QOS NON QUARANTED SUBSCRIPTIONS """
@app.get('/qos_createNoQuarantedSubscription')
async def root():
    response = qos_createNoQuarantedSubscription()
    return response

""" DELETE ALL QOS SUBSCRIPTIONS """
@app.get('/qos_deleteSub', response_class=HTMLResponse)
async def root():
    response = qos_deleteSubscription()
    return response

""" CALLBACK  """
@app.post('/monitoring/callback')
async def update_item(
                payload: dict = Body(...)
            ):
        callbackType = determinCallbacktype(str(payload))
        print("New notification retrieved : " + callbackType)
        #print(payload)
        if(callbackType == "callbacktype = qos"):
            qoss._setStatus(extractQosEvent(str(payload)))
            print(qoss._getStatus())
        else:
            print("Unknown callback type")


""" RETURN QOS STATUS """
@app.get('/qos_getStatus')
async def root():
    return (qoss._getStatus())
