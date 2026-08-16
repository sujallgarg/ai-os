from dataclasses import dataclass, field


@dataclass
class PolicyDecision:

    action: str

    decision: str

    reason: str

    requires_approval: bool = False

    metadata: dict = field(
        default_factory=dict
    )