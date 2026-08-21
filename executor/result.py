from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionResult:

    task_id: int

    status: str

    output: Any = None

    error: str | None = None

    metadata: dict = field(
        default_factory=dict
    )

    approval_id: str | None = None