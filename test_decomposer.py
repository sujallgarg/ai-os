from planner.models import PlanStep

from planner.decomposer import (
    TaskDecomposer
)


decomposer = TaskDecomposer()


step = PlanStep(

    id=1,

    description=(
        "Create a professional "
        "reply to the client."
    ),

    agent="email",

    action="draft_reply",

    parameters={
        "tone": "professional"
    }
)


tasks = decomposer.decompose(
    step
)


print("\nDECOMPOSED TASKS")
print("=" * 70)


for task in tasks:

    print(
        f"\nTask {task.id}"
    )

    print(
        "Description:",
        task.description
    )

    print(
        "Agent:",
        task.agent
    )

    print(
        "Action:",
        task.action
    )

    print(
        "Parameters:",
        task.parameters
    )

    print(
        "Depends on:",
        task.depends_on
    )

    print(
        "Status:",
        task.status
    )