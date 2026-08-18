"""
Agent capability models.
"""

from dataclasses import dataclass, field


@dataclass
class Capability:

    name: str

    description: str = ""

    tools: list[str] = field(
        default_factory=list
    )

    risk_level: str = "low"


@dataclass
class AgentProfile:

    name: str

    description: str

    capabilities: list[str] = field(
        default_factory=list
    )

    tools: list[str] = field(
        default_factory=list
    )

    priority: int = 5

    status: str = "available"