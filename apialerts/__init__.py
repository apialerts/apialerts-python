"""
API Alerts  Wrapper
~~~~~~~~~~~~~~~~~~~

A basic wrapper for the API Alerts API.

:copyright: (c) Copyright 2025 Jared Hall
:license: MIT, see LICENSE for more details.
"""

__title__ = 'apialerts-python'
__author__ = 'apialerts'
__license__ = 'MIT'
__copyright__ = 'Copyright 2025 API Alerts'
__version__ = '1.1.0'

from .apialerts import ApiAlerts
from .models.event import ApiAlertsEvent