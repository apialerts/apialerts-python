import unittest
from src.apialerts.apialerts import ApiAlerts, AlertRequest, ValidationError


class TestApiAlerts(unittest.TestCase):
    def setUp(self):
        self.api_alerts = ApiAlerts()

    def test_validate_api_key(self):
        with self.assertRaises(ValidationError):
            self.api_alerts._ApiAlerts__validate_api_key(None)

    def test_validate_data_tags(self):
        data = AlertRequest(
            message='Payment Received $10',
            channel='my-channel',
            tags="some-tag",
            link=33
        )
        output = self.api_alerts._ApiAlerts__validate_data(data)

        expected = AlertRequest(
            message='Payment Received $10',
            channel='my-channel',
            tags=None,
            link=None
        )
        self.assertEqual(expected, output)
