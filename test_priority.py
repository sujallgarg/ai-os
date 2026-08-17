from planner.models import (
    ExecutionTask
)

from priority.manager import (
    PriorityManager
)


manager = PriorityManager()


tasks = [

    ExecutionTask(

        id=1,

        description=(
            "Check client payment issue"
        ),

        agent="email",

        action="search",

        priority=5
    ),

    ExecutionTask(

        id=2,

        description=(
            "Prepare daily summary"
        ),

        agent="email",

        action="summary",

        priority=5
    ),

    ExecutionTask(

        id=3,

        description=(
            "Handle urgent client request"
        ),

        agent="email",

        action="reply",

        priority=5
    )
]


manager.assign(

    tasks[0],

    level="critical",

    urgency=5,

    importance=5
)


manager.assign(

    tasks[1],

    level="normal"
)


manager.assign(

    tasks[2],

    level="high",

    urgency=3
)


sorted_tasks = manager.sort(
    tasks
)


print("\nTASK PRIORITIES")
print("=" * 60)


for task in sorted_tasks:

    print(
        f"Priority {task.priority}: "
        f"{task.description}"
    )