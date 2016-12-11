import json, requests, logging

import boto

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """ Handles the routing of events to specific event-type handler"""

    try:
        detail = event['detail']
        request_param = detail['requestParameters']
        event_name = detail['eventName']





def send_json(payload={}):
    """send the JSON to the RPi

    Keyword arguments:
    payloathe JSON blob to send to the RPi
    """
    router_dns_name = howinator.dynalias.com
    http_rpi_port = 40070

    request_url = 'http://{dns}:'

    r = requests.post('http://')
