from agents.registry.setup import (
    create_agent_registry
)


registry = (
    create_agent_registry()
)


print("\nREGISTERED AGENTS")
print("=" * 60)


for agent in registry.list_agents():

    print(
        "\nName:",
        agent.name
    )

    print(
        "Description:",
        agent.description
    )

    print(
        "Status:",
        agent.status
    )

    print(
        "Capabilities:"
    )

    for capability in (
        agent.capabilities
    ):

        print(
            "  -",
            capability
        )