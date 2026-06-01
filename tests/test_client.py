from __future__ import annotations

import asyncio
import json
import unittest
import urllib.error
from typing import Any, Dict
from unittest.mock import MagicMock, patch

from apialerts import (
    ApiAlerts,
    Event,
    SendResult,
)
# ApiAlertsClient is intentionally not part of the public API (singleton-only
# surface per SDK Design). Tests reach into the internal module to verify the
# underlying client behaviour the singleton wraps.
from apialerts.client import ApiAlertsClient
from apialerts import network as _network


# ── Helpers ───────────────────────────────────────────────────────────────────

def _mock_response(body: Dict[str, Any]) -> MagicMock:
    mock = MagicMock()
    mock.read.return_value = json.dumps(body).encode('utf-8')
    mock.__enter__ = lambda self: self
    mock.__exit__ = MagicMock(return_value=False)
    return mock


def _success_response(workspace: str = 'My Workspace', channel: str = 'general', warnings=None) -> MagicMock:
    return _mock_response({'workspace': workspace, 'channel': channel, 'warnings': warnings or []})


def _http_error(status: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(url='', code=status, msg='', hdrs={}, fp=None)  # type: ignore[arg-type]


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestApiAlertsClient(unittest.TestCase):

    def tearDown(self) -> None:
        ApiAlerts._reset()

    # ── Validation ─────────────────────────────────────────────────────────────

    def test_empty_api_key_returns_error(self) -> None:
        async def _run() -> None:
            client = ApiAlertsClient('')
            result = await client.send_async(Event(message='test'))
            self.assertFalse(result.success)
            self.assertIn('api key is missing', result.error)
        asyncio.run(_run())

    def test_whitespace_api_key_returns_error(self) -> None:
        async def _run() -> None:
            client = ApiAlertsClient('   ')
            result = await client.send_async(Event(message='test'))
            self.assertFalse(result.success)
            self.assertIn('api key is missing', result.error)
        asyncio.run(_run())

    def test_empty_message_returns_error(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', return_value=_success_response()):
                client = ApiAlertsClient('key')
                result = await client.send_async(Event(message=''))
                self.assertFalse(result.success)
                self.assertIn('message is required', result.error)
        asyncio.run(_run())

    # ── HTTP status codes ──────────────────────────────────────────────────────

    def test_200_returns_send_result(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', return_value=_success_response('W', 'C')):
                client = ApiAlertsClient('key')
                result = await client.send_async(Event(message='test'))
                self.assertTrue(result.success)
                self.assertEqual(result.workspace, 'W')
                self.assertEqual(result.channel, 'C')
                self.assertEqual(result.warnings, [])
        asyncio.run(_run())

    def test_200_returns_warnings(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', return_value=_success_response(warnings=['deprecated'])):
                client = ApiAlertsClient('key')
                result = await client.send_async(Event(message='test'))
                self.assertTrue(result.success)
                self.assertEqual(result.warnings, ['deprecated'])
        asyncio.run(_run())

    def test_400_returns_error(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', side_effect=_http_error(400)):
                client = ApiAlertsClient('key')
                result = await client.send_async(Event(message='test'))
                self.assertFalse(result.success)
                self.assertIn('bad request', result.error)
        asyncio.run(_run())

    def test_401_returns_error(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', side_effect=_http_error(401)):
                client = ApiAlertsClient('key')
                result = await client.send_async(Event(message='test'))
                self.assertFalse(result.success)
                self.assertIn('unauthorized', result.error)
        asyncio.run(_run())

    def test_403_returns_error(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', side_effect=_http_error(403)):
                client = ApiAlertsClient('key')
                result = await client.send_async(Event(message='test'))
                self.assertFalse(result.success)
                self.assertIn('forbidden', result.error)
        asyncio.run(_run())

    def test_429_returns_error(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', side_effect=_http_error(429)):
                client = ApiAlertsClient('key')
                result = await client.send_async(Event(message='test'))
                self.assertFalse(result.success)
                self.assertIn('rate limit exceeded', result.error)
        asyncio.run(_run())

    def test_500_returns_unexpected_status_error(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', side_effect=_http_error(500)):
                client = ApiAlertsClient('key')
                result = await client.send_async(Event(message='test'))
                self.assertFalse(result.success)
                self.assertIn('unexpected status: 500', result.error)
        asyncio.run(_run())

    def test_bad_json_returns_invalid_response_error(self) -> None:
        async def _run() -> None:
            mock = MagicMock()
            mock.read.return_value = b'not json'
            mock.__enter__ = lambda self: self
            mock.__exit__ = MagicMock(return_value=False)
            with patch('urllib.request.urlopen', return_value=mock):
                client = ApiAlertsClient('key')
                result = await client.send_async(Event(message='test'))
                self.assertFalse(result.success)
                self.assertIn('invalid response from server', result.error)
        asyncio.run(_run())

    # ── Request headers ────────────────────────────────────────────────────────

    def test_authorization_header(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', return_value=_success_response()) as mock_open:
                client = ApiAlertsClient('my-api-key')
                await client.send_async(Event(message='test'))
                req = mock_open.call_args[0][0]
                headers = {k.lower(): v for k, v in req.header_items()}
                self.assertEqual(headers['authorization'], 'Bearer my-api-key')
        asyncio.run(_run())

    def test_integration_headers(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', return_value=_success_response()) as mock_open:
                client = ApiAlertsClient('key')
                await client.send_async(Event(message='test'))
                req = mock_open.call_args[0][0]
                headers = {k.lower(): v for k, v in req.header_items()}
                self.assertEqual(headers['x-integration'], 'python')
                self.assertRegex(headers['x-version'], r'^\d+\.\d+\.\d+')
        asyncio.run(_run())

    def test_set_overrides_changes_headers(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', return_value=_success_response()) as mock_open:
                client = ApiAlertsClient('key')
                client.set_overrides('github-actions', '1.0.0', 'http://localhost')
                try:
                    await client.send_async(Event(message='test'))
                except Exception:
                    pass
                req = mock_open.call_args[0][0]
                headers = {k.lower(): v for k, v in req.header_items()}
                self.assertEqual(headers['x-integration'], 'github-actions')
                self.assertEqual(headers['x-version'], '1.0.0')
        asyncio.run(_run())

    def test_api_key_override_uses_provided_key(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', return_value=_success_response()) as mock_open:
                client = ApiAlertsClient('original-key')
                result = await client.send_async(Event(message='test'), api_key='override-key')
                self.assertTrue(result.success)
                req = mock_open.call_args[0][0]
                headers = {k.lower(): v for k, v in req.header_items()}
                self.assertEqual(headers['authorization'], 'Bearer override-key')
        asyncio.run(_run())

    # ── Payload serialization ──────────────────────────────────────────────────

    def test_all_fields_serialized(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', return_value=_success_response('W', 'developer')) as mock_open:
                client = ApiAlertsClient('key')
                await client.send_async(Event(
                    message='Full payload',
                    channel='developer',
                    event='ci.deploy',
                    title='Deployed',
                    tags=['CI/CD', 'Python'],
                    link='https://github.com',
                    data={'version': '2.0.0'},
                ))
                req = mock_open.call_args[0][0]
                body = json.loads(req.data.decode('utf-8'))
                self.assertEqual(body['message'], 'Full payload')
                self.assertEqual(body['channel'], 'developer')
                self.assertEqual(body['event'], 'ci.deploy')
                self.assertEqual(body['title'], 'Deployed')
                self.assertEqual(body['link'], 'https://github.com')
                self.assertEqual(body['data'], {'version': '2.0.0'})
        asyncio.run(_run())

    def test_null_fields_omitted(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', return_value=_success_response()) as mock_open:
                client = ApiAlertsClient('key')
                await client.send_async(Event(message='minimal'))
                req = mock_open.call_args[0][0]
                body = json.loads(req.data.decode('utf-8'))
                self.assertNotIn('channel', body)
                self.assertNotIn('event', body)
                self.assertNotIn('title', body)
                self.assertNotIn('tags', body)
                self.assertNotIn('link', body)
                self.assertNotIn('data', body)
        asyncio.run(_run())

    # ── Fire-and-forget ────────────────────────────────────────────────────────

    def test_send_does_not_raise_on_error(self) -> None:
        with patch('urllib.request.urlopen', side_effect=_http_error(401)):
            client = ApiAlertsClient('key')
            client.send(Event(message='test'))  # must not raise

    def test_send_does_not_raise_on_empty_message(self) -> None:
        client = ApiAlertsClient('key')
        client.send(Event(message=''))  # must not raise

    def test_send_does_not_raise_on_empty_api_key(self) -> None:
        client = ApiAlertsClient('')
        client.send(Event(message='test'))  # must not raise

    # ── Global singleton ───────────────────────────────────────────────────────

    def test_singleton_send_async_returns_error_when_not_configured(self) -> None:
        async def _run() -> None:
            result = await ApiAlerts.send_async(Event(message='test'))
            self.assertFalse(result.success)
            self.assertIn('client not configured', result.error)
        asyncio.run(_run())

    def test_singleton_configure_initializes(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', return_value=_success_response('W', 'C')):
                ApiAlerts.configure('key')
                result = await ApiAlerts.send_async(Event(message='test'))
                self.assertTrue(result.success)
                self.assertEqual(result.workspace, 'W')
        asyncio.run(_run())

    def test_singleton_configure_is_idempotent(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', return_value=_success_response()):
                ApiAlerts.configure('first-key')
                ApiAlerts.configure('second-key')  # should be ignored
                result = await ApiAlerts.send_async(Event(message='test'))
                self.assertIsNotNone(result)
        asyncio.run(_run())

    def test_singleton_send_is_noop_before_configure(self) -> None:
        ApiAlerts.send(Event(message='test'))  # must not raise

    def test_singleton_api_key_override_returns_error_when_not_configured(self) -> None:
        async def _run() -> None:
            result = await ApiAlerts.send_async(Event(message='test'), api_key='key')
            self.assertFalse(result.success)
            self.assertIn('client not configured', result.error)
        asyncio.run(_run())

    def test_singleton_api_key_override_uses_provided_key(self) -> None:
        async def _run() -> None:
            with patch('urllib.request.urlopen', return_value=_success_response()) as mock_open:
                ApiAlerts.configure('original-key')
                result = await ApiAlerts.send_async(Event(message='test'), api_key='override-key')
                self.assertTrue(result.success)
                req = mock_open.call_args[0][0]
                headers = {k.lower(): v for k, v in req.header_items()}
                self.assertEqual(headers['authorization'], 'Bearer override-key')
        asyncio.run(_run())


if __name__ == '__main__':
    unittest.main()
