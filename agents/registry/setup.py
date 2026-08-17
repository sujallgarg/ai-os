from agents.registry.registry import (
    AgentRegistry
)

from agents.registry.default_agents import (
    register_default_agents
)


def create_agent_registry():

    registry = AgentRegistry()

    register_default_agents(
        registry
    )

    return registry