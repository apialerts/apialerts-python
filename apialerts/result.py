from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SendResult:
    """The outcome of a ``send_async`` call.

    ``send_async`` never raises - inspect ``success`` to branch on
    delivery, then read ``workspace`` / ``channel`` on success or
    ``error`` on failure.

    Attributes:
        success: ``True`` if the event was delivered to API Alerts.
        workspace: Workspace name returned by the server. Populated on
            success, ``None`` on failure.
        channel: Channel the event landed on. Populated on success,
            ``None`` on failure.
        warnings: Non-fatal warnings returned by the server (e.g.
            deprecated field usage). Empty list when there are none.
        error: Human-readable error message. Populated on failure,
            ``None`` on success.
    """

    success: bool
    workspace: Optional[str] = None
    channel: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None
