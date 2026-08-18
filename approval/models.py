from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ApprovalStatus(str, Enum):

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass
class ApprovalRequest:

    id: str

    agent_id: str

    tool_name: str

    action: str

    parameters: dict = field(
        default_factory=dict
    )

    reason: str = ""

    status: ApprovalStatus = (
        ApprovalStatus.PENDING
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )