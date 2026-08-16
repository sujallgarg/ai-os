from tool_registry.setup import (
    create_tool_registry
)


registry = create_tool_registry()


print("\nALL REGISTERED TOOLS")
print("=" * 60)


for tool in registry.list_tools():

    print(
        tool.name
    )

    print(
        "Description:",
        tool.description
    )

    print(
        "Agents:",
        tool.agent_types
    )

    print(
        "Approval:",
        tool.requires_approval
    )

    print("-" * 60)