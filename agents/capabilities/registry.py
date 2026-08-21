"""
Agent capability registry.
"""


from agents.capabilities.models import (
    AgentProfile
)


class CapabilityRegistry:

    def __init__(self):

        self.agents = {}

    # ============================================================
    # REGISTER AGENT
    # ============================================================

    def register(
        self,
        agent
    ):

        self.agents[
            agent.name
        ] = agent

    # ============================================================
    # GET AGENT
    # ============================================================

    def get(
        self,
        agent_name
    ):

        return self.agents.get(
            agent_name
        )

    # ============================================================
    # GET ALL AGENTS
    # ============================================================

    def all(self):

        return list(
            self.agents.values()
        )

    # ============================================================
    # FIND BY CAPABILITY
    # ============================================================

    def find_by_capability(
        self,
        capability
    ):

        matches = []

        for agent in self.agents.values():

            if agent.status != "available":

                continue

            if capability in (
                agent.capabilities
            ):

                matches.append(
                    agent
                )

        return matches

    # ============================================================
    # CHECK AGENT
    # ============================================================

    def has_capability(
        self,
        agent_name,
        capability
    ):

        agent = self.get(
            agent_name
        )

        if not agent:

            return False

        return (
            capability
            in agent.capabilities
        )

    def exists(
        self,
        agent_name
    ):

        return (
            agent_name
            in self.agents
        )