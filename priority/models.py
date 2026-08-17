"""
Task priority models.
"""

from dataclasses import dataclass, field


@dataclass
class TaskPriority:

    score: int

    level: str

    reason: str = ""

    metadata: dict = field(
        default_factory=dict
    )