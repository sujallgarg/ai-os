"""
In-memory message bus for agent communication.

For the MVP, messages are stored in memory.
Later this can be replaced with Redis, RabbitMQ,
Kafka, or another production message broker.
"""

from collections import defaultdict, deque


class AgentMessageBus:

    def __init__(self):

        self.queues = defaultdict(
            deque
        )

    def send(
        self,
        message
    ):

        self.queues[
            message.receiver
        ].append(
            message
        )

        print(
            f"[MessageBus] "
            f"{message.sender} → "
            f"{message.receiver}"
        )

    def receive(
        self,
        agent_name: str
    ):

        queue = self.queues[
            agent_name
        ]

        if not queue:

            return None

        return queue.popleft()

    def receive_all(
        self,
        agent_name: str
    ):

        queue = self.queues[
            agent_name
        ]

        messages = []

        while queue:

            messages.append(
                queue.popleft()
            )

        return messages

    def has_messages(
        self,
        agent_name: str
    ):

        return bool(
            self.queues[
                agent_name
            ]
        )