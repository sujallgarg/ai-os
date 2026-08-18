"""
Supervisor models.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SupervisorDecision:

    action: str

    reason: str

    task_id: int | None = None

    metadata: dict = field(
        default_factory=dict
    )


@dataclass
class ExecutionState:

    goal: str

    total_tasks: int

    completed_tasks: int = 0

    failed_tasks: int = 0

    running_tasks: int = 0

    pending_tasks: int = 0

    status: str = "running"

    results: dict[int, Any] = field(
        default_factory=dict
    )