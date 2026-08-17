"""
Agent registry models.
"""

from dataclasses import dataclass, field


@dataclass
class AgentDefinition:

    name: str

    description: str

    capabilities: list[str] = field(
        default_factory=list
    )

    status: str = "available"

    version: str = "1.0.0"

    metadata: dict = field(
        default_factory=dict
    )