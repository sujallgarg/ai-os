"""
Retry system models.
"""

from dataclasses import dataclass, field


@dataclass
class RetryConfig:

    max_attempts: int = 3

    initial_delay: float = 1.0

    max_delay: float = 30.0

    multiplier: float = 2.0

    jitter: float = 0.2


@dataclass
class RetryDecision:

    should_retry: bool

    attempt: int

    delay: float

    reason: str

    error_type: str

    metadata: dict = field(
        default_factory=dict
    )