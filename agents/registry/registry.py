"""
Central Agent Registry.

Keeps track of all available agents and
their capabilities.
"""

from agents.registry.models import (
    AgentDefinition
)


class AgentRegistry:

    def __init__(self):

        self.agents = {}

    def register(
        self,
        definition: AgentDefinition
    ):

        if definition.name in self.agents:

            raise ValueError(
                f"Agent already registered: "
                f"{definition.name}"
            )

        self.agents[
            definition.name
        ] = definition

    def get(
        self,
        name: str
    ):

        agent = self.agents.get(
            name
        )

        if agent is None:

            raise KeyError(
                f"Agent not found: {name}"
            )

        return agent

    def exists(
        self,
        name: str
    ):

        return name in self.agents

    def list_agents(self):

        return list(
            self.agents.values()
        )

    def list_available(self):

        return [

            agent

            for agent in self.agents.values()

            if agent.status == "available"

        ]

    def find_by_capability(
        self,
        capability: str
    ):

        return [

            agent

            for agent in self.agents.values()

            if capability
            in agent.capabilities

        ]

    def set_status(
        self,
        name: str,
        status: str
    ):

        agent = self.get(
            name
        )

        agent.status = status