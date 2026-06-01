from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Event:
    """A single notification dispatched to API Alerts.

    Only ``message`` is required. All other fields are optional and
    omitted from the request body when None.

    Attributes:
        message: Human-readable notification text. Required. This is
            what appears on the push notification lock screen.
        channel: Workspace channel the push notification fires on.
            Defaults to the workspace default channel when omitted.
        event: Identifies what kind of thing happened. Optional but
            recommended. Use dotted notation (e.g.
            ``ci.deploy.success``, ``payment.failed``, ``user.signup``)
            so routing rules can match glob patterns like ``ci.*`` or
            ``*.failed``.
        title: Short headline some destinations render separately from
            the message body.
        tags: Categorisation tags for filtering and search.
        link: URL associated with the event. Available as a deeplink
            for push notifications and as a call-to-action for routed
            destinations.
        data: Arbitrary key-value metadata. Available to non-push
            destinations for templating (Slack message bodies, email
            templates, webhook payloads).
    """

    message: str
    channel: Optional[str] = None
    event: Optional[str] = None
    title: Optional[str] = None
    tags: Optional[List[str]] = None
    link: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

    def _to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {'message': self.message}
        if self.channel is not None:
            result['channel'] = self.channel
        if self.event is not None:
            result['event'] = self.event
        if self.title is not None:
            result['title'] = self.title
        if self.tags is not None:
            result['tags'] = self.tags
        if self.link is not None:
            result['link'] = self.link
        if self.data is not None:
            result['data'] = self.data
        return result
