import unittest
import re

from apialerts.constants import BASE_URL, X_INTEGRATION, X_VERSION


class TestConstants(unittest.TestCase):
    def test_base_url(self):
        self.assertEqual(BASE_URL, "https://api.apialerts.com/event")

    def test_x_integration(self):
        self.assertEqual(X_INTEGRATION, "python")

    def test_x_version(self):
        semver_pattern = r'^\d+\.\d+\.\d+$'
        self.assertTrue(re.match(semver_pattern, X_VERSION), "X_VERSION should be a valid semver")

if __name__ == '__main__':
    unittest.main()