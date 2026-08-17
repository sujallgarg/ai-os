"""
Routes messages between registered agents.
"""


class AgentMessageRouter:

    def __init__(
        self,
        agent_registry,
        message_bus
    ):

        self.registry = (
            agent_registry
        )

        self.bus = (
            message_bus
        )

    def route(
        self,
        message
    ):

        if not self.registry.exists(
            message.receiver
        ):

            raise ValueError(
                f"Agent does not exist: "
                f"{message.receiver}"
            )

        receiver = self.registry.get(
            message.receiver
        )

        if receiver.status != "available":

            raise RuntimeError(
                f"Agent '{message.receiver}' "
                f"is not currently available."
            )

        self.bus.send(
            message
        )