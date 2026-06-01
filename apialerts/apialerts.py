from __future__ import annotations

import logging
import threading
from typing import ClassVar, Optional

from .client import ApiAlertsClient
from .event import Event
from .result import SendResult

_lock = threading.Lock()
_logger = logging.getLogger('apialerts')


class ApiAlerts:
    """Global singleton. Call configure() once at startup."""

    _client: ClassVar[Optional[ApiAlertsClient]] = None

    @classmethod
    def configure(cls, api_key: str, debug: bool = False) -> None:
        """Configure the global client. Subsequent calls are no-ops."""
        with _lock:
            if cls._client is not None:
                return
            cls._client = ApiAlertsClient(api_key, debug=debug)

    @classmethod
    def set_overrides(cls, integration: str, version: str, base_url: str) -> None:
        """Override the X-Integration / X-Version headers and the base URL.

        For wrapper libraries that build on top of this SDK to identify
        themselves (e.g. a Django middleware tagging itself as
        ``django-apialerts``). If a wrapper misbehaves we can tell which
        library is responsible and report it back to its maintainer. Also
        used in tests to redirect at a mock server. Must be called after
        ``configure``.
        """
        if cls._client is not None:
            cls._client.set_overrides(integration, version, base_url)

    @classmethod
    def send(cls, event: Event, api_key: Optional[str] = None) -> None:
        """Fire-and-forget. Never raises. Logs critical errors."""
        if cls._client is None:
            _logger.error('x (apialerts.com) Error: client not configured')
            return
        cls._client.send(event, api_key=api_key)

    @classmethod
    async def send_async(cls, event: Event, api_key: Optional[str] = None) -> SendResult:
        """Awaitable send. Never raises - check result.success instead."""
        if cls._client is None:
            return SendResult(success=False, error='client not configured')
        return await cls._client.send_async(event, api_key=api_key)

    @classmethod
    def _reset(cls) -> None:
        with _lock:
            cls._client = None
