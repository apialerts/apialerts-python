import aiohttp
import certifi
import dataclasses
import json
import ssl
from typing import Any, Dict
from .constants import _X_INTEGRATION, _X_VERSION, _BASE_URL
from .event import ApiAlertsEvent


async def _send_event(api_key: str, payload: ApiAlertsEvent, debug: bool) -> None:
    """
    Send a POST request to the API Alerts service.

    :param api_key: The API key for authentication.
    :param payload: The alert request data.
    :param debug: Enable debug mode if True.
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'X-Integration': _X_INTEGRATION,
        'X-Version': _X_VERSION,
    }

    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        body = dataclasses.asdict(payload)
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(_BASE_URL, headers=headers, json=body) as response:
                if debug:
                    await __handle_response(response)
    except Exception as e:
        if debug:
            print(f'x (apialerts.com) Error: {e}')


async def __handle_response(response: aiohttp.ClientResponse) -> None:
    """
    Handle the response from the API Alerts service.

    :param response: The response object from the POST request.
    """
    response_text = await response.text()
    if response.status == 200 and response_text:
        response_data: Dict[str, Any] = json.loads(response_text)
        workspace = response_data.get('workspace')
        channel = response_data.get('channel')
        print(f'✓ (apialerts.com) Alert sent to {workspace or "?"} ({channel or "?"}).')
        errors = response_data.get('errors') or []
        for error in errors:
            print(f'! (apialerts.com) Warning: {error}')
    elif response.status != 200 and response_text and response_text.startswith('{'):
        response_data: Dict[str, Any] = json.loads(response_text)
        message = response_data.get('message')
        print(f'x (apialerts.com) Error: {message or "?"}')
    else:
        print(f'x (apialerts.com) Error: Something went wrong {response.status}')