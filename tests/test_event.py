import unittest
from apialerts.event import Event, _validate_event

class TestEvent(unittest.TestCase):

    def test_event_initialization(self):
        event = Event(message="Test message")
        self.assertEqual(event.message, "Test message")
        self.assertIsNone(event.channel)
        self.assertIsNone(event.tags)
        self.assertIsNone(event.link)

    def test_event_initialization_with_optional_fields(self):
        event = Event(
            message="Test message",
            channel="Test channel",
            tags=["tag1", "tag2"],
            link="http://example.com"
        )
        self.assertEqual(event.message, "Test message")
        self.assertEqual(event.channel, "Test channel")
        self.assertEqual(event.tags, ["tag1", "tag2"])
        self.assertEqual(event.link, "http://example.com")

    def test_event_validate_valid(self):
        data = Event(
            message='Payment Received $10',
            channel='testing',
            tags=['tag1', 'tag2'],
            link='http://example.com'
        )
        result = _validate_event(data)
        self.assertEqual(result, [])

    def test_event_validate_invalid_all_except_message(self):
        data = Event(
            message='Payment Received $10',
            channel=123,
            tags='tag1',
            link=77
        )
        result = _validate_event(data)
        validations = [
            "! (apialerts.com) Validation: Dropping channel from alert - channel must be a string.",
            "! (apialerts.com) Validation: Dropping tags from alert - tags must be a list of strings",
            "! (apialerts.com) Validation: Dropping link from alert - link must be a list of strings"
        ]
        self.assertEqual(result, validations)

    def test_event_validate_invalid_channel(self):
        data = Event(
            message='Payment Received $10',
            channel=123,
            tags=['tag1', 'tag2'],
            link='http://example.com'
        )
        result = _validate_event(data)
        validations = ["! (apialerts.com) Validation: Dropping channel from alert - channel must be a string."]
        self.assertEqual(result, validations)

    def test_event_validate_invalid_message(self):
        data = Event(
            message=123,
            channel='testing',
            tags=['tag1', 'tag2'],
            link='http://example.com'
        )
        result = _validate_event(data)
        validations = ["x (apialerts.com) Validation: Message must be a string"]
        self.assertEqual(result, validations)

    def test_event_validate_invalid_tags(self):
        data = Event(
            message='Payment Received $10',
            channel='testing',
            tags='tag1',
            link='http://example.com'
        )
        result = _validate_event(data)
        validations = ["! (apialerts.com) Validation: Dropping tags from alert - tags must be a list of strings"]
        self.assertEqual(result, validations)

    def test_event_validate_invalid_link(self):
        data = Event(
            message='Payment Received $10',
            channel='testing',
            tags=['tag1', 'tag2'],
            link=123
        )
        result = _validate_event(data)
        validations = ["! (apialerts.com) Validation: Dropping link from alert - link must be a list of strings"]
        self.assertEqual(result, validations)

if __name__ == '__main__':
    unittest.main()