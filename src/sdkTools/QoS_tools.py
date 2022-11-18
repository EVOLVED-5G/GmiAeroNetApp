from evolved5g.swagger_client.rest import ApiException
from evolved5g.swagger_client import UsageThreshold
from evolved5g.sdk import QosAwareness
from emulator import Emulator_Utils
import os

def qos_createQuarantedSubscription():
    netapp_id = str(os.getenv('NETAPP_ID'))
    qos_awereness = QosAwareness(nef_url=Emulator_Utils.get_url_of_the_nef_emulator(),
                                 nef_bearer_access_token= Emulator_Utils.get_token_for_nef_emulator().access_token,
                                 folder_path_for_certificates_and_capif_api_key=Emulator_Utils.get_folder_path_for_certificated_and_capif_api_key(),
                                 capif_host=Emulator_Utils.get_capif_host(),
                                 capif_https_port=Emulator_Utils.get_capif_https_port())
    equipment_network_identifier = os.environ['REQUESTED_UE_IP']
    network_identifier = QosAwareness.NetworkIdentifier.IP_V4_ADDRESS
    conversational_voice = QosAwareness.GBRQosReference.CONVERSATIONAL_VOICE
    # In this scenario we monitor UPLINK
    uplink = QosAwareness.QosMonitoringParameter.UPLINK
    # Minimum delay of data package during uplink, in milliseconds
    uplink_threshold = 20
    gigabyte = 1024 * 1024 * 1024
    # Up to 10 gigabytes 5 GB downlink, 5gb uplink
    usage_threshold = UsageThreshold(duration= None, # not supported
                                     total_volume=10 * gigabyte,  # 10 Gigabytes of total volume
                                     downlink_volume=5 * gigabyte,  # 5 Gigabytes for downlink
                                     uplink_volume=5 * gigabyte  # 5 Gigabytes for uplink
                                     )
    notification_destination = os.environ['NETAPP_CALLBACK_URL'] 

    subscription = qos_awereness.create_guaranteed_bit_rate_subscription(
        netapp_id=netapp_id,
        equipment_network_identifier=equipment_network_identifier,
        network_identifier=network_identifier,
        notification_destination=notification_destination,
        gbr_qos_reference=conversational_voice,
        usage_threshold=usage_threshold,
        qos_monitoring_parameter=uplink,
        threshold=uplink_threshold,
        #reporting_mode= QosAwareness.EventTriggeredReportingConfiguration(wait_time_in_seconds=3),
        # You can now choose also the PeriodicReportConfiguration for reporting mode
        reporting_mode= QosAwareness.PeriodicReportConfiguration(repetition_period_in_seconds=15)
    )
    # Request information about a subscription
    id = subscription.link.split("/")[-1]
    subscription_info = qos_awereness.get_subscription(netapp_id, id)
    print("--- RETRIEVING INFORMATION ABOUT SUBSCRIPTION " + id + "----")
    print(subscription_info)
    return (subscription_info)

def qos_createNoQuarantedSubscription():
    netapp_id = str(os.getenv('NETAPP_ID'))
    qos_awereness = QosAwareness(nef_url=Emulator_Utils.get_url_of_the_nef_emulator(),
                                 nef_bearer_access_token= Emulator_Utils.get_token_for_nef_emulator().access_token,
                                 folder_path_for_certificates_and_capif_api_key=Emulator_Utils.get_folder_path_for_certificated_and_capif_api_key(),
                                 capif_host=Emulator_Utils.get_capif_host(),
                                 capif_https_port=Emulator_Utils.get_capif_https_port())
    equipment_network_identifier = os.environ['REQUESTED_UE_IP']
    network_identifier = QosAwareness.NetworkIdentifier.IP_V4_ADDRESS
    qos_reference = QosAwareness.NonGBRQosReference.LIVE_STREAMING
    gigabyte = 1024 * 1024 * 1024
    # Up to 10 gigabytes. 5 GB downlink, 5gb uplink
    usage_threshold = UsageThreshold(duration=None,  # not supported
                                     total_volume=10 * gigabyte,  # 10 Gigabytes of total volume
                                     downlink_volume=5 * gigabyte,  # 5 Gigabytes for downlink
                                     uplink_volume=5 * gigabyte  # 5 Gigabytes for uplink
                                     )
    notification_destination = os.environ['NETAPP_CALLBACK_URL']
    subscription = qos_awereness.create_non_guaranteed_bit_rate_subscription(
        netapp_id=netapp_id,
        equipment_network_identifier=equipment_network_identifier,
        network_identifier=network_identifier,
        notification_destination=notification_destination,
        non_gbr_qos_reference=qos_reference,
        usage_threshold=usage_threshold
    )
    print("--- PRINTING THE SUBSCRIPTION WE JUST CREATED ----")
    print(subscription)

    # Request information about a subscription
    id = subscription.link.split("/")[-1]
    subscription_info = qos_awereness.get_subscription(netapp_id, id)
    print("--- RETRIEVING INFORMATION ABOUT SUBSCRIPTION " + id + "----")
    print(subscription_info)
    return(subscription_info)

def qos_deleteSubscription():
    # How to get all subscriptions
    netapp_id = str(os.getenv('NETAPP_ID'))
    qos_awareness = QosAwareness(nef_url=Emulator_Utils.get_url_of_the_nef_emulator(),
                                 nef_bearer_access_token= Emulator_Utils.get_token_for_nef_emulator().access_token,
                                 folder_path_for_certificates_and_capif_api_key=Emulator_Utils.get_folder_path_for_certificated_and_capif_api_key(),
                                 capif_host=Emulator_Utils.get_capif_host(),
                                 capif_https_port=Emulator_Utils.get_capif_https_port())
    try:
        all_subscriptions = qos_awareness.get_all_subscriptions(netapp_id)
        #print(all_subscriptions)      
        nbrOfDeletedSub = 0
        for subscription in all_subscriptions:
            id = subscription.link.split("/")[-1]
            print("QoS : Deleting subscription with id: " + id)
            qos_awareness.delete_subscription(netapp_id, id)
            nbrOfDeletedSub += 1
        if nbrOfDeletedSub > 0:
            return("QoS : " + str(nbrOfDeletedSub) + " subscrition(s) deleted")
    except ApiException as ex:
        if ex.status == 404:
            print("QoS : No active transcriptions found")
            return("QoS : No active transcriptions found")
        else: #something else happened, re-throw the exception
            print("QoS : No active transcriptions found")
            raise

    return("QoS : " + str(nbrOfDeletedSub) + " subscrition(s) deleted")