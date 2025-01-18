from .client import Client
from .event import Event


class ApiAlerts:
    _instance: 'ApiAlerts' = None

    def __init__(self) -> None:
        self.client: Client = Client()

    def __new__(cls, *args, **kwargs) -> 'ApiAlerts':
        if not cls._instance:
            cls._instance = super(ApiAlerts, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def configure(self, api_key: str, debug: bool = False) -> None:
        """Configure the API client with a default API key and debug (logging) mode."""
        self.client.configure(api_key, debug)

    def send(self, data: Event) -> None:
        """Send the alert asynchronously in the background."""
        self.client.send(data)

    async def send_async(self, data: Event) -> None:
        """Send the alert asynchronously and wait for the response. Use send() unless you need to wait for the response."""
        await self.client.send_async(data)

    def send_with_api_key(self, api_key: str, data: Event) -> None:
        """Send the alert asynchronously in the background with a different api key than configure()."""
        self.client.send_with_api_key(api_key, data)

    async def send_with_api_key_async(self, api_key: str, data: Event) -> None:
        """Send the alert asynchronously with a different API key than configure() and wait for the response. Use send_with_api_key() unless you need to wait for the response."""
        await self.client.send_with_api_key_async(api_key, data)
