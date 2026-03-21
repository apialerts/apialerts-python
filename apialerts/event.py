from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Event:
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
