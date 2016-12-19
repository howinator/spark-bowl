import logging
import json
import os

import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """ Handles the routing of events to specific event-type handler"""

    expected_id = os.environ['AlexaApplicationId']

    try:
        app_id_from_event = event['session']['application']['applicationId']
        logger.info("event.session.application.applicationId=" + app_id_from_event)
        expected_app_id = os.environ['ALEXA_APPLICATION_ID']
        if app_id_from_event != expected_app_id:
            raise WrongIdException
    except WrongIdException:
        logger.warning("Wrong Application Id. Expected " +
                       expected_app_id + ". Received " + app_id_from_event)
    if event['session']['new']:


def send_json(payload={}, https=False):
    """send the JSON to the RPi

    Keyword arguments:
    payloathe JSON blob to send to the RPi
    """

    # TODO FIXME This is so screwed up and dangerous - it needs to be fixed asap
    # Probably needs to be doing something like this
    # http://stackoverflow.com/questions/6999565/python-https-get-with-basic-authentication
    router_dns_name = howinator.dynalias.com
    http_rpi_port = 40070
    https_rpi_port = 40071

    if https:
        request_url = 'https://{dns}:{port}'.format(port=router_dns_name, port=https_rpi_port)
    else:
        request_url = 'http://{dns}:{port}'.format(dns=router_dns_name, port=http_rpi_port)

    r = requests.post(http_request_url, data=json.dumps(payload))

    if r.status_code == 200:
        return True
    else:
        return False


class WrongIdException(Exception):
    pass
