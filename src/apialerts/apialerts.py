import aiohttp
import asyncio
import json
from dataclasses import dataclass
from typing import List, Optional
import threading
from .constants import BASE_URL, X_INTEGRATION, X_VERSION


class ValidationError(Exception):
    pass


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


@dataclass
class AlertRequest:
    message: str
    channel: Optional[str] = None
    tags: Optional[List[str]] = None
    link: Optional[str] = None


class ApiAlerts(Singleton):
    _initialized = False

    def __init__(self):
        if ApiAlerts._initialized:
            return
        self.api_key: Optional[str] = None
        self.logging: bool = False
        ApiAlerts._initialized = True

    def configure(self, api_key: Optional[str], logging: bool = False) -> None:
        self.api_key = api_key
        self.logging = logging

    async def send_async(self, data: AlertRequest, api_key: Optional[str] = None) -> None:
        try:
            key = self.__validate_api_key(api_key if api_key else self.api_key)
            payload = self.__validate_data(data)
        except ValidationError as e:
            print(f"! (apialerts.com) Validation: {e}")
            return

        await self.__post(key, payload)

    def send(self, data: AlertRequest, api_key: Optional[str] = None) -> None:
        try:
            key = self.__validate_api_key(api_key if api_key else self.api_key)
            payload = self.__validate_data(data)
        except ValidationError as e:
            print(f"! (apialerts.com) Validation: {e}")
            return

        thread = threading.Thread(target=self.__post_thread, args=(key, payload))
        thread.start()

    def __post_thread(self, api_key: str, payload: AlertRequest) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.__post(api_key, payload))
        loop.close()

    @staticmethod
    def __validate_api_key(api_key: Optional[str]) -> str:
        if api_key is None:
            raise ValidationError("! (apialerts.com) Validation: Workspace API Key not provided")
        elif api_key is not None and not isinstance(api_key, str):
            raise ValidationError("! (apialerts.com) Validation: Workspace API Key must be a string")
        else:
            return api_key

    @staticmethod
    def __validate_data(data: AlertRequest) -> Optional[AlertRequest]:

        # Validate message
        if not isinstance(data.message, str):
            raise ValidationError("! (apialerts.com) Validation: message must be a string")

        # Validate tags
        if data.tags is not None:
            if not isinstance(data.tags, list) or not all(isinstance(tag, str) for tag in data.tags):
                print("! (apialerts.com) Validation: tags must be a list of strings")
                data.tags = None

        # Validate link
        if data.link is not None and not isinstance(data.link, str):
            print("! (apialerts.com) Validation: link must be a string")
            data.link = None

        # Data is validated
        return data

    async def __post(self, api_key: str, payload: AlertRequest) -> None:

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Integration": X_INTEGRATION,
            "X-Version": X_VERSION,
        }
        payload = {
            'channel': payload.channel,
            'message': payload.message,
            'tags': payload.tags,
            'link': payload.link
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(BASE_URL, headers=headers, json=payload) as response:
                    if self.logging:
                        response_text = await response.text()
                        response_data = json.loads(response_text)
                        if response.status == 200:
                            workspace = response_data.get('workspace')
                            channel = response_data.get('channel')
                            errors = response_data.get('errors') or []
                            print(f"✓ (apialerts.com) Alert sent to {workspace or '?'} ({channel or '?'}).")
                            for error in errors:
                                print(f" (apialerts.com) Warning: {error}")
                        else:
                            error_message = response_data.get('message') or "",
                            print(f"x (apialerts.com) Error: {error_message}")
        except Exception as e:
            if self.logging:
                print(f"x (apialerts.com) Error: {e}")
