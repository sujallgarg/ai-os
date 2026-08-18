"""
Models for tool permission resolution.
"""

from dataclasses import dataclass, field
from enum import Enum


class PermissionDecision(str, Enum):

    ALLOW = "ALLOW"

    ASK_USER = "ASK_USER"

    DENY = "DENY"


@dataclass
class ToolRequest:

    agent_id: str

    tool_name: str

    action: str

    parameters: dict = field(
        default_factory=dict
    )

    risk_level: str = "low"


@dataclass
class PermissionResult:

    decision: PermissionDecision

    reason: str

    requires_approval: bool = False

    metadata: dict = field(
        default_factory=dict
    )