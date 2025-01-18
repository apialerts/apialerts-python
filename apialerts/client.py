import asyncio
from typing import Optional

from .models.event import ApiAlertsEvent
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

    def send(self, data: ApiAlertsEvent) -> None:
        """
        Send the alert asynchronously using the configured API key.

        :param data: The alert request data.
        """
        if not self.api_key:
            print('x (apialerts.com) Error: API Key not provided. Use configure() to set a default key, or pass the key as a parameter to the send_with_api_key function.')
            return
        self.send_with_api_key(self.api_key, data)

    async def send_async(self, data: ApiAlertsEvent) -> None:
        """
        Send the alert asynchronously using the configured API key.

        :param data: The alert request data.
        """
        if not self.api_key:
            print('x (apialerts.com) Error: API Key not provided. Use configure() to set a default key, or pass the key as a parameter to the send_with_api_key_async function.')
            return
        await self.send_with_api_key_async(self.api_key, data)

    def send_with_api_key(self, api_key: str, data: ApiAlertsEvent) -> None:
        """
        Send the alert asynchronously using a specified API key.

        :param api_key: The API key for authentication.
        :param data: The alert request data.
        """
        validations = self.validate_event(data)
        if self.debug:
            for validation in validations:
                print(validation)
        if data.message == '':
            return

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(send_event(api_key, data, self.debug))
        loop.run_until_complete(asyncio.sleep(0))

    async def send_with_api_key_async(self, api_key: str, data: ApiAlertsEvent) -> None:
        """
        Send the alert asynchronously using a specified API key.

        :param api_key: The API key for authentication.
        :param data: The alert request data.
        """
        validations = self.validate_event(data)
        if self.debug:
            for validation in validations:
                print(validation)
        if data.message == '':
            return

        await send_event(api_key, data, self.debug)

    @staticmethod
    def validate_event(event: ApiAlertsEvent) -> [str]:
        """
        Validates and updates the event request data.
        Drops properties if they are not the correct type.

        :return: An array of validation warnings if any.
        """
        validations: [str] = []

        if not isinstance(event.message, str):
            event.message = ''
            validations += ['x (apialerts.com) Validation: Message must be a string']
        if not isinstance(event.channel, str):
            event.channel = None
            validations += ['! (apialerts.com) Validation: Dropping channel from alert - channel must be a string.']
        if event.tags is not None and not isinstance(event.tags, list):
            event.tags = None
            validations += ['! (apialerts.com) Validation: Dropping tags from alert - tags must be a list of strings']
        if event.link is not None and not isinstance(event.link, str):
            event.link = None
            validations += ['! (apialerts.com) Validation: Dropping link from alert - link must be a list of strings']

        return validations