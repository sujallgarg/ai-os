from recovery.manager import (
    RecoveryManager
)

from planner.models import (
    ExecutionTask
)


manager = RecoveryManager(
    max_retries=3
)


task = ExecutionTask(

    id=100,

    description=(
        "Build the client website"
    ),

    agent="coding",

    action="build",

    parameters={}
)


print("\nTEST: REPLANNING")
print("=" * 60)


decision = manager.handle_failure(

    task_id=task.id,

    error=(
        "Missing dependency. "
        "Current approach cannot complete."
    ),

    task=task
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
    "Replan:",
    decision.replan_request
)