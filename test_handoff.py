from agents.registry.setup import (
    create_agent_registry
)

from communication.manager import (
    AgentCommunicationManager
)

from communication.handoff import (
    AgentHandoffService
)


registry = (
    create_agent_registry()
)


# For this test, make coding available.
coding = registry.get(
    "coding"
)

coding.status = "available"


communication = (
    AgentCommunicationManager(
        registry
    )
)


handoff_service = (
    AgentHandoffService(

        registry,

        communication
    )
)


handoff = handoff_service.handoff(

    task_id=101,

    from_agent="email",

    to_agent="coding",

    objective=(
        "Build the client's "
        "landing page."
    ),

    context={

        "framework": "Next.js",

        "style": "premium",

        "responsive": True
    },

    reason=(
        "Client requested a "
        "new landing page."
    )
)


print("\nHANDOFF CREATED")
print("=" * 60)

print(
    handoff
)


received = communication.receive(
    "coding"
)


print("\nCODING AGENT RECEIVED")
print("=" * 60)

print(
    received
)


accepted = handoff_service.accept(

    handoff.handoff_id
)


print("\nHANDOFF ACCEPTED")
print("=" * 60)

print(
    accepted
)


completed = handoff_service.complete(

    handoff.handoff_id
)


print("\nHANDOFF COMPLETED")
print("=" * 60)

print(
    completed
)