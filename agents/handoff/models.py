"""
Models for agent handoffs.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class HandoffRequest:

    handoff_id: str

    task_id: int

    from_agent: str

    to_agent: str

    objective: str

    context: dict = field(
        default_factory=dict
    )

    reason: str = ""

    created_at: str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )

    status: str = "pending"