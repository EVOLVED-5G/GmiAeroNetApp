import datetime
import os

from evolved5g.sdk import LocationSubscriber
from evolved5g.swagger_client.rest import ApiException

from emulator import Emulator_Utils

def location_getCellId(external_id :str):
    """
    This function request the UE Cell location via the 5G-API
    """
    location_subscriber = LocationSubscriber(nef_url=Emulator_Utils.get_url_of_the_nef_emulator(),
                                             folder_path_for_certificates_and_capif_api_key=Emulator_Utils.get_folder_path_for_certificated_and_capif_api_key(),
                                             capif_host=Emulator_Utils.get_capif_host(),
                                             capif_https_port=Emulator_Utils.get_capif_https_port())
    netapp_id = str(os.getenv('NETAPP_ID'))
    location_info = location_subscriber.get_location_information(
        netapp_id=netapp_id,
        external_id=external_id)
    return(location_info)

def location_getLatAndLon(_cell_id :str):
    """
    This function request the coordonate of the cell
    """
    """Old 2nd parameter : nef_bearer_access_token= Emulator_Utils.get_token_for_nef_emulator().access_token,"""
    location_subscriber = LocationSubscriber(nef_url=Emulator_Utils.get_url_of_the_nef_emulator(),
                                             folder_path_for_certificates_and_capif_api_key=Emulator_Utils.get_folder_path_for_certificated_and_capif_api_key(),
                                             capif_host=Emulator_Utils.get_capif_host(),
                                             capif_https_port=Emulator_Utils.get_capif_https_port())
    location_info = location_subscriber.get_coordinates_of_cell(cell_id=_cell_id)
    return(location_info)

def create_single_request_for_location_info(external_id :str):
    """
    This function request the device Cell location via the 5G-API
    """
    location_subscriber = LocationSubscriber(nef_url=Emulator_Utils.get_url_of_the_nef_emulator(),  
                                             folder_path_for_certificates_and_capif_api_key=Emulator_Utils.get_folder_path_for_certificated_and_capif_api_key(),
                                             capif_host=Emulator_Utils.get_capif_host(),
                                             capif_https_port=Emulator_Utils.get_capif_https_port())
    netapp_id = str(os.getenv('NETAPP_ID'))
    location_info = location_subscriber.get_location_information(
        netapp_id=netapp_id,
        external_id=external_id
    )
    print(location_info)
    return(location_info)

def location_create_sub(external_id :str):
    # Create a subscription, that will notify us 1000 times, for the next 1 day starting from now
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).isoformat() + "Z"

    location_subscriber = LocationSubscriber(nef_url=Emulator_Utils.get_url_of_the_nef_emulator(),
                                             folder_path_for_certificates_and_capif_api_key=Emulator_Utils.get_folder_path_for_certificated_and_capif_api_key(),
                                             capif_host=Emulator_Utils.get_capif_host(),
                                             capif_https_port=Emulator_Utils.get_capif_https_port())

    netapp_id = str(os.getenv('NETAPP_ID'))
    subscription = location_subscriber.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination = os.environ['NEF_CALLBACK_URL'] ,
        maximum_number_of_reports=1,
        monitor_expire_time=expire_time 
    )
    print(subscription)
    return(subscription) 

def location_delete_sub():
    # get all subscriptions
    location_subscriber = LocationSubscriber(nef_url=Emulator_Utils.get_url_of_the_nef_emulator(),
                                             folder_path_for_certificates_and_capif_api_key=Emulator_Utils.get_folder_path_for_certificated_and_capif_api_key(),
                                             capif_host=Emulator_Utils.get_capif_host(),
                                             capif_https_port=Emulator_Utils.get_capif_https_port())
    netapp_id = str(os.getenv('NETAPP_ID'))
    try:
        all_subscriptions = location_subscriber.get_all_subscriptions(netapp_id, 0, 100)
        print(all_subscriptions)

        for subscription in all_subscriptions:
            id = subscription.link.split("/")[-1]
            print("Deleting subscription with id: " + id)
            location_subscriber.delete_subscription(netapp_id, id)
            return("Deleting subscription with id: " + id)
    except ApiException as ex:
        if ex.status == 404:
            print("No active transcriptions found")
            return ("No active transcriptions found")
        else: #something else happened, re-throw the exception
            raise