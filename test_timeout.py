import time

from timeout.manager import (
    TimeoutManager
)

from timeout.executor import (
    TimeoutExecutor
)

from planner.models import (
    ExecutionTask
)


timeout_manager = (
    TimeoutManager()
)


executor = TimeoutExecutor(
    timeout_manager
)


task = ExecutionTask(

    id=1,

    description=(
        "Test slow agent"
    ),

    agent="email",

    action="slow_test"
)


def slow_function():

    print(
        "Agent started..."
    )

    time.sleep(40)

    print(
        "Agent finished."
    )

    return {
        "success": True
    }


timeout_result, result = (
    executor.run(

        task,

        slow_function
    )
)


print("\nRESULT")
print("=" * 60)

print(
    timeout_result
)

print(
    "Output:",
    result
)