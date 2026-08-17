from parallel.executor import (
    ParallelExecutor
)

from parallel.models import (
    ParallelTask
)


class MockAgentManager:

    def execute(
        self,
        agent_name,
        task
    ):

        import time

        print(
            f"Running {agent_name}..."
        )

        time.sleep(2)

        return {

            "agent":
                agent_name,

            "action":
                task["action"],

            "success":
                True
        }


manager = MockAgentManager()


executor = ParallelExecutor(

    manager,

    max_workers=3
)


tasks = [

    ParallelTask(

        task_id=1,

        agent="email",

        action="search",

        description=(
            "Find important emails"
        )
    ),

    ParallelTask(

        task_id=2,

        agent="calendar",

        action="today",

        description=(
            "Check today's calendar"
        )
    ),

    ParallelTask(

        task_id=3,

        agent="browser",

        action="search",

        description=(
            "Find requested information"
        )
    )
]


results = executor.execute(
    tasks
)


print("\nRESULTS")
print("=" * 60)


for result in results:

    print(
        result
    )