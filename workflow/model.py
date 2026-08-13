"""
Workflow data models.
"""

from dataclasses import dataclass, field


@dataclass
class WorkflowRule:

    name: str

    conditions: dict

    action: str

    action_config: dict = field(
        default_factory=dict
    )

    enabled: bool = True

