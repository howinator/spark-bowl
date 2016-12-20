from __future__ import print_function
import logging
import json
import os

import boto3
import requests
from dotmap import DotMap

import auxiliary as aux


logger = aux.set_logger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """ Handles the routing of events to specific event-type handler"""

    event = DotMap(event)

    try:
        expected_app_id = os.environ['ALEXA_APPLICATION_ID']
    except KeyError as e:
        log_string = "Could not find alexa application id in environment {excp}".format(excp=e)
        logger.error(log_string)
        raise

    try:
        if 'session' not in event:
            raise KeyError
        app_id_from_event = event.session.application.applicationId
        logger.info("event.session.application.applicationId=" + app_id_from_event)
        expected_app_id = os.environ['ALEXA_APPLICATION_ID']
        if app_id_from_event != expected_app_id:
            raise aux.WrongApplicationIdException
    except KeyError as e:
        logger.error("'session' not found in event: %s", e)
        raise
    except aux.WrongApplicationIdException as e:
        logger.warning("Wrong Application Id. Expected " +
                       expected_app_id + ". Received " + app_id_from_event +
                       ". Thrown Exception %s", e)
        raise
    if event.session.new:
        on_session_started({requestId: event.request.requestId})


def send_json(payload={}, https=False):
    """send the JSON to the RPi

    Keyword arguments:
    payloathe JSON blob to send to the RPi
    """
    # TODO FIXME This is so screwed up and dangerous - it needs to be fixed asap
    # Probably needs to be doing something like this
    # http://stackoverflow.com/questions/6999565/python-https-get-with-basic-authentication
    router_dns_name = 'howinator.dynalias.com'
    http_rpi_port = 40070
    https_rpi_port = 40071

    if https:
        request_url = 'https://{dns}:{port}'.format(dns=router_dns_name, port=https_rpi_port)
    else:
        request_url = 'http://{dns}:{port}'.format(dns=router_dns_name, port=http_rpi_port)

    r = requests.post(http_request_url, data=json.dumps(payload))

    if r.status_code == 200:
        return True
    else:
        return False
