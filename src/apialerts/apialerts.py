import aiohttp
import asyncio
import json
from dataclasses import dataclass
from typing import List, Optional


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

    def send(self, data: AlertRequest, api_key: Optional[str] = None) -> None:
        try:
            key = self.__validate_api_key(api_key if api_key else self.api_key)
            payload = self.__validate_data(data)
        except ValidationError as e:
            print(f"APIAlerts -> {e}")
            return
        asyncio.run(self.__post(key, payload))

    @staticmethod
    def __validate_api_key(api_key: Optional[str]) -> str:
        if api_key is None:
            raise ValidationError("Project API Key not provided")
        elif api_key is not None and not isinstance(api_key, str):
            raise ValidationError("Project API Key must be a string")
        else:
            return api_key

    @staticmethod
    def __validate_data(data: AlertRequest) -> Optional[AlertRequest]:

        # Validate message
        if not isinstance(data.message, str):
            raise ValidationError("APIAlerts -> message must be a string")

        # Validate tags
        if data.tags is not None:
            if not isinstance(data.tags, list) or not all(isinstance(tag, str) for tag in data.tags):
                print("APIAlerts -> tags must be a list of strings")
                data.tags = None

        # Validate link
        if data.link is not None and not isinstance(data.link, str):
            print("APIAlerts -> link must be a string")
            data.link = None

        # Data is validated
        return data

    async def __post(self, api_key: str, payload: AlertRequest) -> None:

        url = "https://api.apialerts.com/event"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Integration": "python",
            "X-Version": "0.0.1",
        }
        payload = {
            'message': payload.message,
            'tags': payload.tags,
            'link': payload.link
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if self.logging:
                        response_text = await response.text()
                        response_data = json.loads(response_text)
                        if response.status == 200:
                            project = response_data.get('project')
                            remaining = response_data.get('remainingQuota2')
                            errors = response_data.get('errors') or []
                            print(f"APIAlerts -> Successfully sent event to {project or '?'}. Remaining Quota = {remaining or '?'}")
                            for error in errors:
                                print(f"APIAlerts Warning -> {error}")
                        else:
                            error_message = response_data.get('message') or "",
                            print(f"APIAlerts -> Error: {error_message}")
        except Exception as e:
            if self.logging:
                print(f"APIAlerts -> Error: {e}")
