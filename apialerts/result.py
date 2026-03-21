from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SendResult:
    success: bool
    workspace: Optional[str] = None
    channel: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None
