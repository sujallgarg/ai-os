"""
Central Tool Registry.

All AI tools should be registered here before
agents are allowed to use them.
"""

from tool_registry.models import (
    ToolDefinition
)

from tool_registry.permissions import (
    ToolPermissionManager
)


class ToolRegistry:

    def __init__(self):

        self.tools = {}

        self.permissions = (
            ToolPermissionManager()
        )

    def register(
        self,
        tool: ToolDefinition
    ):

        if tool.name in self.tools:

            raise ValueError(
                f"Tool already registered: "
                f"{tool.name}"
            )

        self.tools[
            tool.name
        ] = tool

    def get(
        self,
        name: str
    ):

        tool = self.tools.get(
            name
        )

        if not tool:

            raise KeyError(
                f"Tool not found: {name}"
            )

        return tool

    def list_tools(
        self
    ):

        return list(
            self.tools.values()
        )

    def list_for_agent(
        self,
        agent_type: str
    ):

        return [
            tool

            for tool in self.tools.values()

            if self.permissions.can_use(
                tool,
                agent_type
            )
        ]

    def execute(
        self,
        name: str,
        agent_type: str,
        **kwargs
    ):

        tool = self.get(
            name
        )

        if not self.permissions.can_use(
            tool,
            agent_type
        ):

            raise PermissionError(
                f"Agent '{agent_type}' "
                f"cannot use tool '{name}'."
            )

        return tool.execute(
            **kwargs
        )