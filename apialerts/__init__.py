"""
API Alerts Python SDK
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) Copyright 2025 API Alerts
:license: MIT
"""

__title__ = 'apialerts'
__author__ = 'apialerts'
__license__ = 'MIT'
__copyright__ = 'Copyright 2025 API Alerts'
__version__ = '1.2.0'

from .apialerts import ApiAlerts
from .event import Event
from .result import SendResult

__all__ = [
    'ApiAlerts',
    'Event',
    'SendResult',
]
