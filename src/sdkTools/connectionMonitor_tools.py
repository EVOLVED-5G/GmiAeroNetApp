from evolved5g.swagger_client.rest import ApiException
from evolved5g.sdk import ConnectionMonitor
from emulator import Emulator_Utils
import datetime
import os

def connection_createSubscription():
    _netapp_id = str(os.getenv('NETAPP_ID'))
    connection_monitor = ConnectionMonitor(nef_url=Emulator_Utils.get_url_of_the_nef_emulator(),
                                           folder_path_for_certificates_and_capif_api_key=Emulator_Utils.get_folder_path_for_certificated_and_capif_api_key(),
                                           capif_host=Emulator_Utils.get_capif_host(),
                                           capif_https_port=Emulator_Utils.get_capif_https_port()   )
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=10)).isoformat() + "Z"
    external_id = "10001@domain.com"
    print("EXTID : " + external_id)
    subscription_when_not_connected = connection_monitor.create_subscription(
        netapp_id=_netapp_id,
        external_id=external_id,
        notification_destination = os.environ['NEF_CALLBACK_URL'] ,
        monitoring_type= ConnectionMonitor.MonitoringType.INFORM_WHEN_NOT_CONNECTED,
        wait_time_before_sending_notification_in_seconds=3,
        maximum_number_of_reports=50,
        monitor_expire_time=expire_time
    )
    subscription_when_connected = connection_monitor.create_subscription(
        netapp_id=_netapp_id,
        external_id=external_id,
        notification_destination = os.environ['NEF_CALLBACK_URL'] ,
        monitoring_type= ConnectionMonitor.MonitoringType.INFORM_WHEN_CONNECTED,
        wait_time_before_sending_notification_in_seconds=3,
        maximum_number_of_reports=50,
        monitor_expire_time=expire_time
    )
    return str(subscription_when_not_connected) + "<br><br>" + str(subscription_when_connected)      

def connection_deleteSubscription():
    netapp_id = str(os.getenv('NETAPP_ID'))
    connection_monitor = ConnectionMonitor(nef_url=Emulator_Utils.get_url_of_the_nef_emulator(),
                                           folder_path_for_certificates_and_capif_api_key=Emulator_Utils.get_folder_path_for_certificated_and_capif_api_key(),
                                           capif_host=Emulator_Utils.get_capif_host(),
                                           capif_https_port=Emulator_Utils.get_capif_https_port())
    try:
        all_subscriptions = connection_monitor.get_all_subscriptions(netapp_id, 0, 100)
        #print(all_subscriptions)

        nbrOfDeletedSub = 0
        for subscription in all_subscriptions:
            id = subscription.link.split("/")[-1]
            print("ConnectionMonitor : Deleting subscription with id: " + id)
            connection_monitor.delete_subscription(netapp_id, id)
            nbrOfDeletedSub += 1
        if nbrOfDeletedSub > 0:
            return("ConnectionMonitor : " + str(nbrOfDeletedSub) + " subscrition(s) deleted")
    except ApiException as ex:
        if ex.status == 404:
            print("ConnectionMonitor : No active transcriptions found")
            return("ConnectionMonitor : No active transcriptions found")
        else: #something else happened, re-throw the exception
            print("ConnectionMonitor : No active transcriptions found")
            raise

    return("ConnectionMonitor : " + str(nbrOfDeletedSub) + " subscrition(s) deleted")

