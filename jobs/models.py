from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class JobStatus(str, Enum):

    QUEUED = "queued"
    RUNNING = "running"
    WAITING_FOR_APPROVAL = "waiting_for_approval"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Job:

    id: str

    goal: str

    status: JobStatus = JobStatus.QUEUED

    progress: float = 0.0

    current_task_id: int | None = None

    pending_approval_id: str | None = None

    task_state: dict = field(
        default_factory=dict
    )

    result: object = None

    error: str | None = None

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )