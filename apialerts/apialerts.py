from __future__ import annotations

import sys
import threading
from typing import ClassVar, Optional

from .client import ApiAlertsClient
from .event import Event
from .result import SendResult

_lock = threading.Lock()


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
        if cls._client is not None:
            cls._client.set_overrides(integration, version, base_url)

    @classmethod
    def send(cls, event: Event) -> None:
        """Fire-and-forget. Never raises. Logs critical errors to stderr."""
        if cls._client is None:
            print('x (apialerts.com) Error: client not configured', file=sys.stderr)
            return
        cls._client.send(event)

    @classmethod
    async def send_async(cls, event: Event) -> SendResult:
        """Awaitable send. Never raises — check result.success instead."""
        if cls._client is None:
            return SendResult(success=False, error='client not configured')
        return await cls._client.send_async(event)

    @classmethod
    async def send_with_key_async(cls, api_key: str, event: Event) -> SendResult:
        """Awaitable send with a key override. Never raises — check result.success instead."""
        if cls._client is None:
            return SendResult(success=False, error='client not configured')
        return await cls._client.send_with_key_async(api_key, event)

    @classmethod
    def _reset(cls) -> None:
        with _lock:
            cls._client = None
