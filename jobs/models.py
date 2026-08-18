from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class JobStatus(str, Enum):

    QUEUED = "queued"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


@dataclass
class Job:

    id: str

    goal: str

    status: JobStatus = (
        JobStatus.QUEUED
    )

    progress: float = 0.0

    created_at: datetime = (
        datetime.utcnow()
    )

    result: object = None

    error: str | None = None