"""
High-level agent communication manager.
"""

import uuid

from communication.models import (
    AgentMessage
)

from communication.bus import (
    AgentMessageBus
)

from communication.router import (
    AgentMessageRouter
)


class AgentCommunicationManager:

    def __init__(
        self,
        agent_registry
    ):

        self.bus = (
            AgentMessageBus()
        )

        self.router = (
            AgentMessageRouter(
                agent_registry,
                self.bus
            )
        )

    def send(
        self,
        sender: str,
        receiver: str,
        message_type: str,
        content,
        correlation_id=None,
        metadata=None
    ):

        message = AgentMessage(

            message_id=str(
                uuid.uuid4()
            ),

            sender=sender,

            receiver=receiver,

            message_type=message_type,

            content=content,

            correlation_id=(
                correlation_id
            ),

            metadata=(
                metadata or {}
            )
        )

        self.router.route(
            message
        )

        return message

    def receive(
        self,
        agent_name: str
    ):

        return self.bus.receive(
            agent_name
        )

    def receive_all(
        self,
        agent_name: str
    ):

        return self.bus.receive_all(
            agent_name
        )