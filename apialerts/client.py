from __future__ import annotations

import asyncio
import sys
import threading

from . import network
from .event import Event
from .result import SendResult


class ApiAlertsClient:
    """Instance-based client. Use the ApiAlerts singleton for typical use."""

    def __init__(self, api_key: str, debug: bool = False) -> None:
        self._api_key = api_key
        self._debug = debug
        self._integration = network._INTEGRATION
        self._version = network._VERSION
        self._base_url = network._BASE_URL

    def set_overrides(self, integration: str, version: str, base_url: str) -> None:
        self._integration = integration
        self._version = version
        self._base_url = base_url

    def send(self, event: Event) -> None:
        """Fire-and-forget. Never raises. Critical errors always logged to stderr."""
        try:
            if not self._api_key or not self._api_key.strip():
                print('x (apialerts.com) Error: api key is missing', file=sys.stderr)
                return
            if not event.message or not event.message.strip():
                print('x (apialerts.com) Error: message is required', file=sys.stderr)
                return

            def _run() -> None:
                try:
                    result = self._post(self._api_key, event)
                    if self._debug:
                        if result.success:
                            print(
                                f'✓ (apialerts.com) Alert sent to {result.workspace} ({result.channel})',
                                file=sys.stderr,
                            )
                            for w in result.warnings:
                                print(f'! (apialerts.com) Warning: {w}', file=sys.stderr)
                        else:
                            print(f'x (apialerts.com) Error: {result.error}', file=sys.stderr)
                except Exception as exc:
                    if self._debug:
                        print(f'x (apialerts.com) Error: {exc}', file=sys.stderr)

            threading.Thread(target=_run, daemon=True).start()
        except Exception as exc:
            if self._debug:
                print(f'x (apialerts.com) Error: {exc}', file=sys.stderr)

    async def send_async(self, event: Event) -> SendResult:
        """Awaitable send. Never raises — check result.success instead."""
        try:
            if not self._api_key or not self._api_key.strip():
                return SendResult(success=False, error='api key is missing')
            if not event.message or not event.message.strip():
                return SendResult(success=False, error='message is required')
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, lambda: self._post(self._api_key, event))
            if self._debug:
                if result.success:
                    print(
                        f'✓ (apialerts.com) Alert sent to {result.workspace} ({result.channel})',
                        file=sys.stderr,
                    )
                    for w in result.warnings:
                        print(f'! (apialerts.com) Warning: {w}', file=sys.stderr)
                else:
                    print(f'x (apialerts.com) Error: {result.error}', file=sys.stderr)
            return result
        except Exception as exc:
            return SendResult(success=False, error=str(exc))

    async def send_with_key_async(self, api_key: str, event: Event) -> SendResult:
        """Awaitable send with a key override. Never raises — check result.success instead."""
        try:
            if not api_key or not api_key.strip():
                return SendResult(success=False, error='api key is missing')
            if not event.message or not event.message.strip():
                return SendResult(success=False, error='message is required')
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, lambda: self._post(api_key, event))
            if self._debug:
                if result.success:
                    print(
                        f'✓ (apialerts.com) Alert sent to {result.workspace} ({result.channel})',
                        file=sys.stderr,
                    )
                    for w in result.warnings:
                        print(f'! (apialerts.com) Warning: {w}', file=sys.stderr)
                else:
                    print(f'x (apialerts.com) Error: {result.error}', file=sys.stderr)
            return result
        except Exception as exc:
            return SendResult(success=False, error=str(exc))

    def _post(self, api_key: str, event: Event) -> SendResult:
        return network.post(
            api_key=api_key,
            event=event,
            integration=self._integration,
            version=self._version,
            base_url=self._base_url,
        )
