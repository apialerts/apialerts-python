import unittest

from apialerts.client import Client


class TestClient(unittest.TestCase):
    def test_client_init(self):
        client = Client()
        self.assertIsNone(client.api_key)
        self.assertEqual(client.debug, False)

    def test_client_configure(self):
        client = Client()
        self.assertIsNone(client.api_key)
        self.assertEqual(client.debug, False)

        client.configure("my-api-key", True)
        self.assertEqual(client.api_key, "my-api-key")
        self.assertEqual(client.debug, True)

if __name__ == '__main__':
    unittest.main()
