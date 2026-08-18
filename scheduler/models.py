from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScheduledTask:

    id: str

    task_data: dict

    run_at: datetime

    recurring: bool = False

    interval_seconds: int | None = None

    enabled: bool = True