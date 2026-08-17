"""
Models for communication between AI agents.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class AgentMessage:

    message_id: str

    sender: str

    receiver: str

    message_type: str

    content: Any

    created_at: str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )

    correlation_id: str | None = None

    metadata: dict = field(
        default_factory=dict
    )