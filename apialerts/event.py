from dataclasses import dataclass
from typing import Optional, List

@dataclass
class ApiAlertsEvent:
    """
    Represents a request to send an event to the api alerts service

    Attributes:
        message (str): The event message to be sent.
        channel (Optional[str]): The channel through which the event will be sent.
        tags (Optional[List[str]]): A list of tags associated with the alert.
        link (Optional[str]): An optional link related to the alert.
    """
    message: str
    channel: Optional[str] = None
    tags: Optional[List[str]] = None
    link: Optional[str] = None