import json, requests, logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """ Handles the routing of events to specific

    try:
        detail = event['detail']
        request_param = detail['requestParameters']
        event_name = detail['eventName']
