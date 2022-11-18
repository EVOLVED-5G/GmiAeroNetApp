import os
import sys

from fastapi import FastAPI, Body
from fastapi.responses import FileResponse, HTMLResponse

from header_file import *
from formatTools.str_tools import *
from sdkTools.connectionMonitor_tools import *
from sdkTools.location_tools import *
from sdkTools.QoS_tools import *
from qos_info import *

app = FastAPI()

qoss = QOSINFO()

# Call me only when working locally for dev/debug
def add_local_env_var():
    print("Set local vars : ...OK")
    os.environ['NETAPP_NAME'] = "GMI_Netapp"
    os.environ['NETAPP_ID'] = "gmi_netapp"
    os.environ['NETAPP_PORT_VAPP'] = "8000"
    os.environ['NETAPP_CALLBACK_URL'] = "http://host.docker.internal:8000/monitoring/callback"     #"http://127.0.0.1:5656/monitoring/callback"
    os.environ['NEF_HOST'] = "http://localhost:8888"
    os.environ['NEF_CALLBACK_URL'] = "http://host.docker.internal:"
    os.environ['REQUESTED_UE_IP'] = "10.0.0.1"
    os.environ['REQUESTED_UE_EXTID'] = "10001@domain.com"
 
@app.on_event("startup")
async def startup_event():
    #print("Argument List:", str(sys.argv))
    if(str(sys.argv).rfind("workers") > -1):  #if argument "workers" is passed, thuis is a local run, so call add_local_env_var()
        add_local_env_var()
    print_initmess()
    
""" DEFAULT RESPONSE """
@app.get('/', response_class=HTMLResponse)
async def root():
    return FileResponse('.\html\default.html')

""" RETURN CELL ID AFTER SENDING AN UE ID """
@app.get('/location_getCellID/{externalId}')
async def root(externalId: str): 
   response = location_getCellId(externalId)
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
