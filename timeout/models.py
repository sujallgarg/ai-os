"""
Timeout models.
"""

from dataclasses import dataclass


@dataclass
class TimeoutConfig:

    timeout_seconds: int = 30

    retry_on_timeout: bool = True

    max_timeout_retries: int = 2


@dataclass
class TimeoutResult:

    task_id: int

    status: str

    duration_seconds: float

    error: str | None = None