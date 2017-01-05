import os
import unittest

from mock import patch

import index
import auxiliary as aux


class TestIndex(unittest.TestCase):

    def setUp(self):
        self.context = {"context": "here"}
        fake_app_id = "amzn.ask.skill.fakeappid"
        self.alexa_start = {
            "version": "1.0",
            "session": {
                "sessionId": "SessionId.f2c7b713-5b55-45b8-9bb0-483515e9f47a",
                "application": {
                    "applicationId": fake_app_id
                },
                "attributes": {},
                "user": {
                    "userId": "amzn1.ask.account.AJ5833"
                },
                "new": True
            },
            "request": {
                "type": "LaunchRequest",
                "requestId": "Ed2RequestId.ca22",
                "locale": "en-us",
                "timestamp": "2016-12-11T04:04:44Z"
            }
        }
        self.alexa_feed_dogs = {
            "session": {
                "sessionId": "SessionId.f2c7b713-5b55-45b8-9bb0-483515e9f47a",
                "application": {
                    "applicationId": fake_app_id
                },
                "attributes": {},
                "user": {
                    "userId": "amzn1.ask.account.AGSV"
                },
                "new": False
            },
            "request": {
                "type": "IntentRequest",
                "requestId": "EdwRequestId.d1a5",
                "locale": "en-US",
                "timestamp": "2016-12-11T04:23:00Z",
                "intent": {
                    "name": "FeedDogsIntent",
                    "slots": {}
                }
            },
            "version": "1.0"
        }
        self.end_session = {'request': {}, 'session': {}}
        self.env_patch = patch.dict('os.environ', {'ALEXA_APPLICATION_ID': fake_app_id})
        self.env_patch.start()

    def tearDown(self):
        self.env_patch.stop()

    def test_no_application_id(self):
        self.env_patch.stop()
        with self.assertRaises(KeyError):
            index.lambda_handler(self.alexa_start, self.context)

    def test_session_dne(self):
        bad_event = {"howie": "number_one"}
        with self.assertRaises(KeyError):
            index.lambda_handler(bad_event, self.context)

    def test_bad_app_id(self):
        self.alexa_start['session']['application']['applicationId'] = 'bad'
        with self.assertRaises(aux.WrongApplicationIdException):
            index.lambda_handler(self.alexa_start, self.context)

    @patch('index.on_session_started')
    def test_on_session_started_called(self, index_mock):
        index.lambda_handler(self.alexa_start, self.context)
        index_mock.assert_called_with({'requestId': self.alexa_start['request']['requestId'],
                                       'sessionId': self.alexa_start['session']['sessionId']},
                                      self.alexa_start['session'])

    @patch('index.on_launch')
    def test_on_launch_called(self, index_mock):
        index.lambda_handler(self.alexa_start, self.context)
        index_mock.assert_called_with(launch_request=self.alexa_start[
                                      'request'], session=self.alexa_start['session'])

    @patch('index.on_intent')
    def test_on_intent_called(self, index_mock):
        index.lambda_handler(self.alexa_feed_dogs, self.context)
        index_mock.assert_called_with(
            intent_request=self.alexa_feed_dogs['request'],
            session=self.alexa_feed_dogs['session'])

    @unittest.skip("don't know what end session request looks like")
    @patch('index.on_session_ended')
    def test_on_session_ended_called(self, index_mock):
        index.lambda_handler(self.end_session, self.context)
        index_mock.assert_called_with(end_request=self.end_session[
                                      'request'], session=self.end_session['session'])

    def test_build_speechlet_response(self):
        output = "here's a string"
        title = "stuff"
        reprompt = "some more stuff"
        should_end = False
        expected = {
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
                    "text": reprompt
                }
            },
            "shouldEndSession": should_end
        }
        self.assertEqual(index.build_speechlet_response(
            title, output, reprompt, should_end), expected)

    def test_build_response(self):
        attributes = {"howie": "cool"}
        response = {"howie": "super"}
        expected = {"version": "1.0",
                    "sessionAttributes": attributes, "response": response}
        self.assertEqual(index.build_response(attributes, response), expected)

    def test_download_file(self):
        downloaded_file = index.download_file_from_s3('howinator-config', 'test/test.yml')
        print(downloaded_file)
        with open(downloaded_file) as f:
            assert f.read() == 'sparkabowl_secret_key: testvalue\n'

    def test_get_secret_key(self):
        s3_env_patch = patch.dict(
            'os.environ', {'CONFIG_BUCKET_NAME': 'howinator-config',
                           'CONFIG_FILE_PATH': 'test/test.yml',
                           'CONFIG_KEY_ROLE_ARN': 'arn:aws:iam::742524706181:role/ConfigKeyAccess'})
        s3_env_patch.start()
        self.assertEqual(index.get_secret_key(), 'testvalue')
        s3_env_patch.stop()

    @patch('index.feed_dogs_handler')
    def test_feed_dogs_intent(self, index_mock):
        intent_request = self.alexa_feed_dogs['request']
        intent_session = self.alexa_feed_dogs['session']
        index.on_intent(intent_request=intent_request, session=intent_session)
        index_mock.assert_called_with(request=intent_request, session=intent_session)

    @unittest.skip("functionality not implemented yet")
    def testSendJSON(self):
        json_to_send = {"feedDogs": "True"}
        result = index.send_json(json_to_send, https=False)
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
