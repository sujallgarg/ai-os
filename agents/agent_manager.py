"""
Central Agent Manager.

Registers agents and routes tasks to the
appropriate agent.
"""

from typing import Any


class AgentManager:

    def __init__(self):

        self.agents = {}

    def register(
        self,
        name: str,
        agent: Any
    ):

        if not name:

            raise ValueError(
                "Agent name is required."
            )

        if name in self.agents:

            raise ValueError(
                f"Agent already registered: {name}"
            )

        self.agents[name] = agent

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

    def list_agents(self):

        return list(
            self.agents.keys()
        )

    def execute(
        self,
        agent_name: str,
        task: dict
    ):

        if not isinstance(
            task,
            dict
        ):

            raise TypeError(
                "Task must be a dictionary."
            )

        if not task.get("action"):

            raise ValueError(
                "Task action is required."
            )

        agent = self.get(
            agent_name
        )

        if not hasattr(
            agent,
            "execute"
        ):

            raise AttributeError(
                f"Agent '{agent_name}' "
                "does not support execute()."
            )

        return agent.execute(
            task
        )