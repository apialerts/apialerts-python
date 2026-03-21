from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Dict

from .event import Event
from .result import SendResult

_INTEGRATION = 'python'
_VERSION = '2.0.0'
_BASE_URL = 'https://api.apialerts.com/event'


def post(
    api_key: str,
    event: Event,
    integration: str = _INTEGRATION,
    version: str = _VERSION,
    base_url: str = _BASE_URL,
) -> SendResult:
    body = json.dumps(event._to_dict()).encode('utf-8')
    req = urllib.request.Request(
        url=base_url,
        data=body,
        method='POST',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Integration': integration,
            'X-Version': version,
        },
    )
    try:
        with urllib.request.urlopen(req) as response:
            raw: str = response.read().decode('utf-8')
    except urllib.error.HTTPError as exc:
        return _result_for_status(exc.code)
    except Exception as exc:
        return SendResult(success=False, error=str(exc))

    try:
        data: Dict[str, Any] = json.loads(raw)
        warnings = data.get('warnings') or []
        return SendResult(
            success=True,
            workspace=data.get('workspace'),
            channel=data.get('channel'),
            warnings=warnings if isinstance(warnings, list) else [],
        )
    except (KeyError, json.JSONDecodeError):
        return SendResult(success=False, error='invalid response from server')


def _result_for_status(status: int) -> SendResult:
    if status == 400:
        return SendResult(success=False, error='bad request')
    if status == 401:
        return SendResult(success=False, error='unauthorized — check your api key')
    if status == 403:
        return SendResult(success=False, error='forbidden')
    if status == 429:
        return SendResult(success=False, error='rate limit exceeded')
    return SendResult(success=False, error=f'unexpected status: {status}')
