"""
Tool permission checks.
"""


class ToolPermissionManager:

    def can_use(
        self,
        tool,
        agent_type: str
    ):

        if not tool.agent_types:

            return True

        return (
            agent_type
            in tool.agent_types
        )