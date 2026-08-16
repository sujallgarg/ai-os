from tool_registry.registry import (
    ToolRegistry
)

from tool_registry.gmail_tools import (
    register_gmail_tools
)


def create_tool_registry():

    registry = ToolRegistry()

    register_gmail_tools(
        registry
    )

    return registry