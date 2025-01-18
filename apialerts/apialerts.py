from .client import Client
from .models.event import ApiAlertsEvent
from typing import Optional


class ApiAlerts:
    _instance: Optional['ApiAlerts'] = None
    _client: Optional[Client] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ApiAlerts, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not ApiAlerts._client:
            ApiAlerts._client = Client()

    @classmethod
    def _ensure_client(cls) -> None:
        """Ensure the client is initialized."""
        if not cls._client:
            cls._client = Client()

    @classmethod
    def configure(cls, api_key: str, debug: bool = False) -> None:
        """Configure the API client with a default API key and debug (logging) mode."""
        cls._ensure_client()
        cls._client.configure(api_key, debug)

    @classmethod
    def send(cls, data: ApiAlertsEvent) -> None:
        """Send the alert asynchronously in the background."""
        cls._ensure_client()
        cls._client.send(data)

    @classmethod
    async def send_async(cls, data: ApiAlertsEvent) -> None:
        """Send the alert asynchronously and wait for the response."""
        cls._ensure_client()
        await cls._client.send_async(data)

    @classmethod
    def send_with_api_key(cls, api_key: str, data: ApiAlertsEvent) -> None:
        """Send the alert asynchronously in the background with a different API key than configure()."""
        cls._ensure_client()
        cls._client.send_with_api_key(api_key, data)

    @classmethod
    async def send_with_api_key_async(cls, api_key: str, data: ApiAlertsEvent) -> None:
        """Send the alert asynchronously with a different API key than configure() and wait for the response."""
        cls._ensure_client()
        await cls._client.send_with_api_key_async(api_key, data)