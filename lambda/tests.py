import unittest
import index


class TestIndex(unittest.TestCase):

    def setUp(self):
        self.alexa_start = {
            "version": "1.0",
            "session": {
                "sessionId": "SessionId.f2c7b713-5b55-45b8-9bb0-483515e9f47a",
                "application": {
                    "applicationId": "amzn1.ask.skill.a885349b"
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
                    "applicationId": "amzn1.ask.skill.a885349b"
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

    def testSendJSON(self):
        json_to_send = {"feedDogs": "True"}
        result = index.send_json(json_to_send, https=False)
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
