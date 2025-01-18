from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AlertRequest:
    message: str
    channel: Optional[str] = None
    tags: Optional[List[str]] = None
    link: Optional[str] = None

class ValidationError(Exception):
    pass
