import aiohttp
import dataclasses
import json
from typing import Any, Dict
from apialerts.event import Event
from apialerts.constants import X_INTEGRATION, X_VERSION, BASE_URL


async def send_event(api_key: str, payload: Event, debug: bool) -> None:
    """
    Send a POST request to the API Alerts service.

    :param api_key: The API key for authentication.
    :param payload: The alert request data.
    :param debug: Enable debug mode if True.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Integration": X_INTEGRATION,
        "X-Version": X_VERSION,
    }

    try:
        body = dataclasses.asdict(payload)
        async with aiohttp.ClientSession() as session:
            async with session.post(BASE_URL, headers=headers, json=body) as response:
                if debug:
                    await handle_response(response)
    except Exception as e:
        if debug:
            print(f"x (apialerts.com) Error: {e}")


async def handle_response(response: aiohttp.ClientResponse) -> None:
    """
    Handle the response from the API Alerts service.

    :param response: The response object from the POST request.
    """
    response_text = await response.text()
    if response.status == 200 and response_text:
        response_data: Dict[str, Any] = json.loads(response_text)
        workspace = response_data.get('workspace')
        channel = response_data.get('channel')
        print(f"✓ (apialerts.com) Alert sent to {workspace or '?'} ({channel or '?'}).")
        errors = response_data.get('errors') or []
        for error in errors:
            print(f"! (apialerts.com) Warning: {error}")
    elif response.status != 200 and response_text and response_text.startswith('{'):
        response_data: Dict[str, Any] = json.loads(response_text)
        message = response_data.get('message')
        print(f"x (apialerts.com) Error: {message or '?'}")
    else:
        print(f"x (apialerts.com) Error: Something went wrong {response.status}")
