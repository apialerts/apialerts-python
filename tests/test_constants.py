"""Pin literal values of SDK constants. Catches accidental changes to the
integration name, version shape, base URL, or timeout - matches the canonical
pattern documented in SDK Design (one constants test file per SDK).
"""
from __future__ import annotations

import re
import unittest

from apialerts import network as _network


class TestConstants(unittest.TestCase):

    def test_integration_name_is_python(self) -> None:
        self.assertEqual(_network._INTEGRATION, 'python')

    def test_base_url_is_apialerts_event_endpoint(self) -> None:
        self.assertEqual(_network._BASE_URL, 'https://api.apialerts.com/event')

    def test_timeout_is_30_seconds_per_spec(self) -> None:
        self.assertEqual(_network._TIMEOUT_SECONDS, 30)

    def test_version_is_one_x_semver(self) -> None:
        # Major version pin: bumping to v2.x requires updating this test
        # deliberately. Catches accidental major bumps.
        self.assertRegex(_network._VERSION, r'^1\.\d+\.\d+(?:[-+][\w.]+)?$')


if __name__ == '__main__':
    unittest.main()
