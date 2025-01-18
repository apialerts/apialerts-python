import asyncio
from typing import Optional

from .event import Event, _validate_event
from .network.network import send_event


class Client:
    def __init__(self) -> None:
        """
        Initialize the Client with default values.
        """
        self.api_key: Optional[str] = None
        self.debug: bool = False

    def configure(self, api_key: str = None, debug: bool = False) -> None:
        """
        Configure the Client with an API key and debug mode.

        :param api_key: The API key for authentication.
        :param debug: Enable debug mode if True.
        """
        self.api_key = api_key
        self.debug = debug

    def send(self, data: Event) -> None:
        """
        Send the alert asynchronously using the configured API key.

        :param data: The alert request data.
        """
        if not self.api_key:
            print("x (apialerts.com) Error: API Key not provided. Use configure() to set a default key, or pass the key as a parameter to the send_with_api_key/send_with_api_key_async function.")
            return
        self.send_with_api_key(self.api_key, data)

    async def send_async(self, data: Event) -> None:
        """
        Send the alert asynchronously using the configured API key.

        :param data: The alert request data.
        """
        if not self.api_key:
            print("x (apialerts.com) Error: API Key not provided. Use configure() to set a default key, or pass the key as a parameter to the send_with_api_key/send_with_api_key_async function.")
            return
        await self.send_with_api_key_async(self.api_key, data)

    def send_with_api_key(self, api_key: str, data: Event) -> None:
        """
        Send the alert asynchronously using a specified API key.

        :param api_key: The API key for authentication.
        :param data: The alert request data.
        """
        validations = _validate_event(data)
        if self.debug:
            for validation in validations:
                print(validation)
        if data.message == "":
            return

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(send_event(api_key, data, self.debug))
        loop.run_until_complete(asyncio.sleep(0))

    async def send_with_api_key_async(self, api_key: str, data: Event) -> None:
        """
        Send the alert asynchronously using a specified API key.

        :param api_key: The API key for authentication.
        :param data: The alert request data.
        """
        validations = _validate_event(data)
        if self.debug:
            for validation in validations:
                print(validation)
        if data.message == "":
            return

        await send_event(api_key, data, self.debug)
