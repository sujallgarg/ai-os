"""
Models for parallel agent execution.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ParallelTask:

    task_id: int

    agent: str

    action: str

    description: str

    parameters: dict = field(
        default_factory=dict
    )


@dataclass
class ParallelResult:

    task_id: int

    agent: str

    status: str

    output: Any = None

    error: str | None = None