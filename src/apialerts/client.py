# client.py
import aiohttp
import asyncio
import certifi
import json
import ssl

from .models import AlertRequest, ValidationError
from .constants import BASE_URL, X_INTEGRATION, X_VERSION

class Client:
    def __init__(self, api_key: str, debug: bool = False):
        self.api_key = api_key
        self.debug = debug

    def send(self, data: AlertRequest) -> None:
        """Send an alert asynchronously in the background without waiting for the result."""
        self.send_with_api_key(self.api_key, data)

    def send_with_api_key(self, api_key: str, data: AlertRequest) -> None:
        """Send an alert asynchronously in the background with an api key without waiting for the result."""
        try:
            payload = self.__validate_data(data)
        except ValidationError as e:
            print(f"! (apialerts.com) Validation: {e}")
            return

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self.__post(api_key, payload))
        loop.run_until_complete(asyncio.sleep(0))

    async def send_async(self, data: AlertRequest) -> None:
        """Send an alert asynchronously and await the response."""
        await self.send_with_api_key_async(self.api_key, data)

    async def send_with_api_key_async(self, api_key: str, data: AlertRequest) -> None:
        """Send an alert asynchronously with an api key and await the response."""
        try:
            payload = self.__validate_data(data)
        except ValidationError as e:
            print(f"! (apialerts.com) Validation: {e}")
            return

        # Now awaiting the post request
        await self.__post(api_key, payload)

    @staticmethod
    def __validate_data(data: AlertRequest) -> AlertRequest:
        # Validate message, tags, and link as before
        if not isinstance(data.message, str):
            raise ValidationError("Message must be a string")
        if data.tags is not None and not isinstance(data.tags, list):
            raise ValidationError("Tags must be a list of strings")
        if data.link is not None and not isinstance(data.link, str):
            raise ValidationError("Link must be a string")
        return data

    async def __post(self, api_key: str, payload: AlertRequest) -> None:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Integration": X_INTEGRATION,
            "X-Version": X_VERSION,
        }

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
                async with session.post(BASE_URL, headers=headers, json=payload.__dict__) as response:
                    if self.debug:
                        await self.__handle_response(response)
        except Exception as e:
            if self.debug:
                print(f"x (apialerts.com) Error: {e}")

    @staticmethod
    async def __handle_response(response):
        response_text = await response.text()
        if response.status == 200 and response_text:
            response_data = json.loads(response_text)
            workspace = response_data.get('workspace')
            channel = response_data.get('channel')
            print(f"✓ (apialerts.com) Alert sent to {workspace or '?'} ({channel or '?'}).")
            errors = response_data.get('errors') or []
            for error in errors:
                print(f"! (apialerts.com) Warning: {error}")
        elif response.status != 200 and response_text and response_text.startswith('{'):
            response_data = json.loads(response_text)
            message = response_data.get('message')
            print(f"x (apialerts.com) Error: {message or '?'}")
        else:
            print(f"x (apialerts.com) Error: Something went wrong {response.status}")
