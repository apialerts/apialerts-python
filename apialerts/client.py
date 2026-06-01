from __future__ import annotations

import asyncio
import logging
import threading
from typing import Optional

from . import network
from .event import Event
from .result import SendResult


logger = logging.getLogger('apialerts')


class ApiAlertsClient:
    """Instance-based client. Use the ApiAlerts singleton for typical use."""

    def __init__(self, api_key: str, debug: bool = False) -> None:
        self._api_key = api_key
        self._debug = debug
        self._integration = network._INTEGRATION
        self._version = network._VERSION
        self._base_url = network._BASE_URL

    def set_overrides(self, integration: str, version: str, base_url: str) -> None:
        """Override the X-Integration / X-Version headers and the base URL.

        For wrapper libraries that build on top of this SDK to identify
        themselves (e.g. a Django middleware tagging itself as
        ``django-apialerts``). If a wrapper misbehaves we can tell which
        library is responsible and report it back to its maintainer. Also
        used in tests to redirect at a mock server.
        """
        self._integration = integration
        self._version = version
        self._base_url = base_url

    def send(self, event: Event, api_key: Optional[str] = None) -> None:
        """Fire-and-forget. Never raises. Critical errors always logged."""
        try:
            key = api_key if api_key and api_key.strip() else self._api_key
            if not key or not key.strip():
                logger.error('x (apialerts.com) Error: api key is missing')
                return
            if not event.message or not event.message.strip():
                logger.error('x (apialerts.com) Error: message is required')
                return

            def _run() -> None:
                try:
                    result = self._post(key, event)
                    self._log_result(result)
                except Exception as exc:
                    if self._debug:
                        logger.info('x (apialerts.com) Error: %s', exc)

            threading.Thread(target=_run, daemon=True).start()
        except Exception as exc:
            if self._debug:
                logger.info('x (apialerts.com) Error: %s', exc)

    async def send_async(self, event: Event, api_key: Optional[str] = None) -> SendResult:
        """Awaitable send. Never raises - check result.success instead."""
        try:
            key = api_key if api_key and api_key.strip() else self._api_key
            if not key or not key.strip():
                return SendResult(success=False, error='api key is missing')
            if not event.message or not event.message.strip():
                return SendResult(success=False, error='message is required')
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, lambda: self._post(key, event))
            self._log_result(result)
            return result
        except Exception as exc:
            return SendResult(success=False, error=str(exc))

    def _log_result(self, result: SendResult) -> None:
        if not self._debug:
            return
        if result.success:
            logger.info(
                '✓ (apialerts.com) Alert sent to %s (%s)',
                result.workspace,
                result.channel,
            )
            for w in result.warnings:
                logger.info('! (apialerts.com) Warning: %s', w)
        else:
            logger.info('x (apialerts.com) Error: %s', result.error)

    def _post(self, api_key: str, event: Event) -> SendResult:
        return network.post(
            api_key=api_key,
            event=event,
            integration=self._integration,
            version=self._version,
            base_url=self._base_url,
        )
