"""
Tool Registry data models.
"""

from dataclasses import dataclass, field
from typing import Callable, Any


@dataclass
class ToolDefinition:

    name: str

    description: str

    function: Callable

    agent_types: list[str] = field(
        default_factory=list
    )

    requires_approval: bool = False

    metadata: dict = field(
        default_factory=dict
    )

    def execute(
        self,
        **kwargs: Any
    ):

        return self.function(
            **kwargs
        )