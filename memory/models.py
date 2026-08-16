"""
Memory data models.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Memory:

    id: str

    user_id: str

    memory_type: str

    key: str

    value: str

    importance: float = 0.5

    created_at: str = ""

    updated_at: str = ""

    source: str = "user"