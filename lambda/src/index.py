from __future__ import print_function
import logging
import json
import os
import tempfile
import yaml

import boto3
import botocore
from cryptography.fernet import Fernet
import requests

import auxiliary as aux


logger = aux.set_logger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """ Handles the routing of events to specific event-type handler"""
    try:
        expected_app_id = os.environ['ALEXA_APPLICATION_ID']
    except KeyError as e:
        log_string = "Could not find alexa application id in environment {excp}".format(excp=e)
        logger.error(log_string)
        raise
    try:
        if not all(k in event for k in ('request', 'session')):
            raise KeyError
        request = event['request']
        session = event['session']
        app_id_from_event = session['application']['applicationId']
        logger.info("event.session.application.applicationId=" + app_id_from_event)
        expected_app_id = os.environ['ALEXA_APPLICATION_ID']
        if app_id_from_event != expected_app_id:
            raise aux.WrongApplicationIdException
    except KeyError as e:
        logger.error("'session' or 'request' not found in event: %s", e)
        raise
    except aux.WrongApplicationIdException as e:
        logger.warning("Wrong Application Id. Expected " +
                       expected_app_id + ". Received " + app_id_from_event +
                       ". Thrown Exception %s", e)
        raise

    if session['new']:
        on_session_started({'requestId': request['requestId'],
                            'sessionId': session['sessionId']}, session)

    if request['type'] == 'LaunchRequest':
        return on_launch(launch_request=request, session=session)
    elif request['type'] == 'IntentRequest':
        return on_intent(intent_request=request, session=session)
    elif request['type'] == 'SessionEndedRequest':
        return on_session_ended(end_request=request, session=session)


def on_session_started(event_ids, session):
    logger.info("New session with session id: %s and request id: %s",
                event_ids['sessionId'], event_ids['requestId'])


def on_launch(launch_request, session):
    return get_welcome_response()


def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent['name']

    if intent_name == "FeedDogsIntent":
        return feed_dogs_handler(request=intent_request, session=session)


def on_session_ended(request, session):
    return True


def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome to Sparkabowl!"
    speech_output = "Welcome to the Sparkabowl skill. " \
                    "You can ask me to feed the dog."
    reprompt_text = "Please ask me to feed the dog."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def feed_dogs_handler(request, session):
    rpi_payload = build_rpi_payload(request)
    send_status = send_json_to_rpi(rpi_payload)
    session_attributes = {}
    reprompt_text = ''
    if send_status:
        speech_output = 'Dogs have been fed. Yay!'
        card_title = 'Dogs have been fed!'
        should_end_session = True
    else:
        speech_output = 'Something went wrong. You need to feed the dogs manually.'
        card_title = 'DOGS HAVE NOT BEEN FED'
        should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }


def build_rpi_payload(request):
    payload = {}
    encrypted_access_key = get_and_encrypt_access_key()
    payload['key'] = encrypted_access_key
    if request['intent']['name'] == 'FeedDogsIntent':
        sub_payload = build_feed_now_payload()
    # more intents to come
    else:
        logger.error('No valid intent')
        raise aux.NoValidIntent

    payload = aux.merge_two_dicts(payload, sub_payload)

    return payload


def build_feed_now_payload():
    sub_payload = {}
    sub_payload['type'] = 'FeedDogsNow'

    return sub_payload


def download_file_from_s3(s3_bucket, s3_key, credentials=None):
    download_path = tempfile.mkdtemp()
    base_name = os.path.basename(s3_key)
    download_path = '{}/{}'.format(download_path, base_name)

    if credentials is not None:
        config = botocore.client.Config(signature_version='s3v4')
        s3_resource = boto3.resource('s3',
                                     aws_access_key_id=credentials['AccessKeyId'],
                                     aws_secret_access_key=credentials['SecretAccessKey'],
                                     aws_session_token=credentials['SessionToken'],
                                     config=config)
    else:
        s3_resource = boto3.resource('s3')

    try:
        s3_resource.Bucket(s3_bucket).download_file(s3_key, download_path)
    except botocore.exceptions.ClientError as e:
        logger.error(
            "Something went wrong with downloading the {}/{} file to {}\n{}".format(
                s3_bucket, s3_key, download_path, e))
        raise

    # s3_client = boto3.client('s3', config=botocore.client.Config(signature_version='s3v4'))
    # try:
    #     s3_client.download_file(s3_bucket, s3_key, download_path)
    # except botocore.exceptions.ClientError as e:
    #     logger.error(
    #         "Something went wrong with downloading the {}/{} file to {}\n{}".format(
    #             s3_bucket, s3_client, download_path, e))
    #     raise

    return download_path


def get_secret_key():
    try:
        config_bucket = os.environ['CONFIG_BUCKET_NAME']
        config_path = os.environ['CONFIG_FILE_PATH']
    except KeyError as e:
        logger.error('Could not find config info in env\n{}'.format(e))
        raise

    sts_client = boto3.client('sts')
    try:
        config_role_arn = os.environ['CONFIG_KEY_ROLE_ARN']
    except KeyError as e:
        logger.error('Could not find ARN of config_key_role in environment\n{}'.format(e))
        raise
    assumedRoleObject = sts_client.assume_role(
        RoleArn=config_role_arn,
        RoleSessionName='AssumedRoleLambdaConfigKey')
    config_key_credentials = assumedRoleObject['Credentials']
    config_file_path = download_file_from_s3(config_bucket, config_path, config_key_credentials)

    with open(config_file_path, 'r') as f:
        try:
            config_info = yaml.load(f)
        except yaml.YAMLError as e:
            logger.error('Could not parse config yaml\n{}'.format(e))
            raise

    try:
        secret_key = config_info['sparkabowl_secret_key']
    except KeyError as e:
        logger.error('Config file malformed: sparkabowl_secret_key not found\n{}'.format(e))

    return secret_key


def get_and_encrypt_access_key():

    secret_key = get_secret_key()

    access_key = os.environ['SPARKABOWL_ACCESS_KEY']

    f = Fernet(secret_key)
    token = f.encrypt(access_key)

    return token


def send_json_to_rpi(payload, https=False):
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

    r = requests.post(request_url, json=payload)

    if r.status_code == 200:
        return True
    else:
        return False
