from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Event:
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


def _validate_event(event: 'Event') -> [str]:
    """
    Validates and updates the event request data.
    Drops properties if they are not the correct type.

    :return: An array of validation warnings if any.
    """
    validations: [str] = []

    if not isinstance(event.message, str):
        event.message = ""
        validations += ["x (apialerts.com) Validation: Message must be a string"]
    if not isinstance(event.channel, str):
        event.channel = None
        validations += ["! (apialerts.com) Validation: Dropping channel from alert - channel must be a string."]
    if event.tags is not None and not isinstance(event.tags, list):
        event.tags = None
        validations += ["! (apialerts.com) Validation: Dropping tags from alert - tags must be a list of strings"]
    if event.link is not None and not isinstance(event.link, str):
        event.link = None
        validations += ["! (apialerts.com) Validation: Dropping link from alert - link must be a list of strings"]

    return validations
