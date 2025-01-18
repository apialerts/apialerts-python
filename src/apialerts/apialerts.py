from .client import Client
from .models import AlertRequest

class ApiAlerts:
    _instance = None

    def __init__(self):
        self.client = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ApiAlerts, cls).__new__(cls, *args, **kwargs)
            cls._instance.client = None
        return cls._instance

    def configure(self, api_key: str, debug: bool = False) -> None:
        self.client = Client(api_key, debug)

    def send(self, data: AlertRequest) -> None:
        """Send the alert asynchronously in the background."""
        if not self.client:
            print("ApiAlerts not configured. Call configure() first.")
            return
        self.client.send(data)

    async def send_async(self, data: AlertRequest) -> None:
        """Send the alert asynchronously and wait for the response."""
        if not self.client:
            print("ApiAlerts not configured. Call configure() first.")
            return
        await self.client.send_async(data)

    def send_with_api_key(self, api_key: str, data: AlertRequest) -> None:
        """Send the alert asynchronously with a different api key than configure() in the background."""
        if not self.client:
            print("ApiAlerts not configured. Call configure() first.")
            return
        self.client.send_with_api_key(api_key, data)

    async def send_with_api_key_async(self, api_key: str, data: AlertRequest) -> None:
        """Send the alert asynchronously with a different api key than configure() and wait for the response."""
        if not self.client:
            print("ApiAlerts not configured. Call configure() first.")
            return
        await self.client.send_with_api_key_async(api_key, data)

