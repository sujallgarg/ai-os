from agents.registry.setup import (
    create_agent_registry
)

from communication.manager import (
    AgentCommunicationManager
)


registry = (
    create_agent_registry()
)


communication = (
    AgentCommunicationManager(
        registry
    )
)


message = communication.send(

    sender="email",

    receiver="coding",

    message_type="task_request",

    content={
        "task": (
            "Create a landing page "
            "for the client."
        ),

        "requirements": [

            "Responsive design",

            "Professional UI",

            "Use Next.js"
        ]
    }
)


print("\nMESSAGE SENT")
print("=" * 60)

print(
    message
)


received = communication.receive(
    "coding"
)


print("\nMESSAGE RECEIVED")
print("=" * 60)

print(
    received
)