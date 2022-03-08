from evolved5g.swagger_client.rest import ApiException
from evolved5g.sdk import LocationSubscriber
from emulator import Emulator_Utils
import datetime

class location_sub:
    subName = ""
    extID = ""
    cellID = ""

def create_single_request_for_location_info(external_id :str):
    """
    This function request the device location via the 5G-API
    """
    netapp_id = "GMI-AERO_Netapp"
    host = Emulator_Utils.get_host_of_the_nef_emulator()
    token = Emulator_Utils.get_token()
    location_subscriber = LocationSubscriber(host, token.access_token)

    location_info = location_subscriber.get_location_information(
        netapp_id=netapp_id,
        external_id=external_id
    )
    print(location_info)
    return location_info

def read_and_delete_all_existing_loc_subscriptions():
    # How to get all subscriptions
    netapp_id = "GMI-AERO_Netapp"
    host = Emulator_Utils.get_host_of_the_nef_emulator()
    token = Emulator_Utils.get_token()
    location_subscriber = LocationSubscriber(host, token.access_token)

    try:
        all_subscriptions = location_subscriber.get_all_subscriptions(netapp_id, 0, 100)
        print(all_subscriptions)

        for subscription in all_subscriptions:
            id = subscription.link.split("/")[-1]
            location_subscriber.delete_subscription(netapp_id, id)
            print("Deleting subscription with id: " + id)
            return ("Deleting subscription with id: " + id)
            
    except ApiException as ex:
        if ex.status == 404:
            print("No active transcriptions found")
            return ("No active transcriptions found")
        else: #something else happened, re-throw the exception
            raise

def create_subscription_and_retrieve_call_backs(external_id :str):
    # Create a subscription, that will notify us 1000 times, for the next 1 day starting from now
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z"
    netapp_id = "GMI-AERO_Netapp"
    host = Emulator_Utils.get_host_of_the_nef_emulator()
    token = Emulator_Utils.get_token()
    location_subscriber = LocationSubscriber(host, token.access_token)

    subscription = location_subscriber.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination="http://host.docker.internal:8000/monitoring/callback",
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time
    )

    # From now on we should retrieve POST notifications to http://host.docker.internal:5000/monitoring/loc_callback

    print(subscription)

    # How to get all subscriptions
    all_subscriptions = location_subscriber.get_all_subscriptions(netapp_id, 0, 100)
    print(all_subscriptions)

    # Request information about a subscription
    id = subscription.link.split("/")[-1]
    subscription_info = location_subscriber.get_subscription(netapp_id, id)
    # print(subscription_info)
    return subscription_info 