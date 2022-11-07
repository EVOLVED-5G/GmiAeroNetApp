from evolved5g.swagger_client.rest import ApiException
from evolved5g.sdk import QosAwareness
from emulator import Emulator_Utils
from evolved5g.swagger_client import UsageThreshold

class qos_sub:
    ipv4addr = ""
    event = ""
    transaction = ""

def read_and_delete_all_existing_qos_subscriptions():
    # How to get all subscriptions
    netapp_id = "GmiAeroNetapp"
    host = Emulator_Utils.get_host_of_the_nef_emulator()
    token = Emulator_Utils.get_token()
    qos_awareness = QosAwareness(host, token.access_token)

    qos_sub.ipv4addr = ""
    qos_sub.event = ""
    qos_sub.transaction = ""

    try:
        all_subscriptions = qos_awareness.get_all_subscriptions(netapp_id)
        print(all_subscriptions)

        for subscription in all_subscriptions:
            id = subscription.link.split("/")[-1]
            print("Deleting subscription with id: " + id)
            qos_awareness.delete_subscription(netapp_id, id)
            return ("Deleting subscription with id: " + id)
    except ApiException as ex:
        if ex.status == 404:
            print("No active transcriptions found")
        else: #something else happened, re-throw the exception
            raise

def create_non_quaranteed_bit_rate_subscription_for_live_streaming():
    """
    This example showcases how you can create a subscription to the 5G-API in order to establish
    a Non-Guaranteed Bit Rate (NON-GBR) QoS.
    In order to run this example you need to follow the instructions in  readme.md in order to a) run the NEF emulator
    and b) run a local webserver that will print the location notifications it retrieves from the emulator.
    A testing local webserver (Flask webserver) can be initiated by running the examples/api.py
    """

    # Create a subscription, that will notify us 1000 times, for the next 1 day starting from now
    netapp_id = "GmiAeroNetapp"
    host = Emulator_Utils.get_host_of_the_nef_emulator()
    token = Emulator_Utils.get_token()
    qos_awereness = QosAwareness(host, token.access_token)
    # The following external identifier was copy pasted by the NEF emulator. Go to the Map and hover over a User icon.
    # There you can retrieve the id address
    equipment_network_identifier = "10.0.0.1"
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

    # In this example we are running flask at http://localhost:5000 with a POST route to (/monitoring/qos_callback) in order to retrieve notifications.
    # If you are running on the NEF emulator, you need to provide a notification_destination with an IP that the
    # NEF emulator docker can understand
    # For latest versions of docker this should be: http://host.docker.internal:5000/monitoring/callback"
    # Alternative you can find the ip of the HOST by running 'ip addr show | grep "\binet\b.*\bdocker0\b" | awk '{print $2}' | cut -d '/' -f 1'
    # See article for details: https://stackoverflow.com/questions/48546124/what-is-linux-equivalent-of-host-docker-internal/61001152
    notification_destination="http://host.docker.internal:8000/monitoring/qos_callback"
    subscription = qos_awereness.create_guaranteed_bit_rate_subscription(
        netapp_id=netapp_id,
        equipment_network_identifier=equipment_network_identifier,
        network_identifier=network_identifier,
        notification_destination=notification_destination,
        gbr_qos_reference=conversational_voice,
        usage_threshold=usage_threshold,
        qos_monitoring_parameter=uplink,
        threshold=uplink_threshold,
        wait_time_between_reports=10

    )
    # From now on we should retrieve POST notifications to http://host.docker.internal:8000/monitoring/qos_callback

    print("--- PRINTING THE SUBSCRIPTION WE JUST CREATED ----")
    print(subscription)

    # Request information about a subscription
    id = subscription.link.split("/")[-1]
    subscription_info = qos_awereness.get_subscription(netapp_id, id)
    print("--- RETRIEVING INFORMATION ABOUT SUBSCRIPTION " + id + "----")
    print(subscription_info)
    return subscription_info