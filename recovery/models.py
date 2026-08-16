"""
Error recovery models.
"""

from dataclasses import dataclass, field


@dataclass
class RecoveryDecision:

    action: str

    reason: str

    retry_count: int = 0

    modified_parameters: dict = field(
        default_factory=dict
    )