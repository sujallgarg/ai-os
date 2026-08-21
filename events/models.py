from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class SystemEvent:

    event: str

    job_id: str | None = None

    task_id: int | None = None

    agent_id: str | None = None

    data: dict[str, Any] = field(
        default_factory=dict
    )

    timestamp: str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )

    def to_dict(self):

        return {
            "event": self.event,
            "job_id": self.job_id,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "data": self.data,
            "timestamp": self.timestamp,
        }