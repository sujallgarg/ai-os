from supervisor.supervisor import (
    SupervisorAgent
)


class MockTask:

    def __init__(
        self,
        task_id
    ):

        self.id = task_id


tasks = [

    MockTask(1),

    MockTask(2),

    MockTask(3)
]


supervisor = SupervisorAgent()


print(
    "\nSTARTING SUPERVISOR"
)

print(
    "=" * 60
)


state = supervisor.start(

    goal=(
        "Handle client website request"
    ),

    tasks=tasks
)


print(
    state
)


# --------------------------------
# Task 1
# --------------------------------

supervisor.task_started(
    1
)

supervisor.task_completed(

    1,

    result={
        "success": True
    }
)


# --------------------------------
# Task 2
# --------------------------------

supervisor.task_started(
    2
)

supervisor.task_completed(

    2,

    result={
        "success": True
    }
)


# --------------------------------
# Task 3
# --------------------------------

supervisor.task_started(
    3
)

supervisor.task_completed(

    3,

    result={
        "success": True
    }
)


# --------------------------------
# Supervisor decision
# --------------------------------

decision = supervisor.decide(
    []
)


print(
    "\nSUPERVISOR DECISION"
)

print(
    "=" * 60
)

print(
    "Action:",
    decision.action
)

print(
    "Reason:",
    decision.reason
)


print(
    "\nFINAL STATE"
)

print(
    supervisor.get_state()
)