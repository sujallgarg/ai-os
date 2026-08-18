"""
Models used by the shared agent memory system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class Memory:

    key: str

    value: Any

    agent_id: str

    memory_type: str = "shared"

    importance: int = 5

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )

    expires_at: Optional[datetime] = None

    metadata: dict = field(
        default_factory=dict
    )