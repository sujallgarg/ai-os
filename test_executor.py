from planner.models import (
    ExecutionTask
)

from executor.executor import (
    TaskExecutor
)


class MockAgentManager:

    def execute(
        self,
        agent_name,
        task
    ):

        print(
            f"[Mock] Agent: {agent_name}"
        )

        print(
            f"[Mock] Action: "
            f"{task['action']}"
        )

        return {
            "success": True,
            "message": (
                f"Executed {task['action']}"
            )
        }


agent_manager = (
    MockAgentManager()
)


executor = TaskExecutor(
    agent_manager
)


tasks = [

    ExecutionTask(

        id=1,

        description="Search Gmail",

        agent="email",

        action="search",

        parameters={
            "query": "proposal"
        },

        depends_on=[]
    ),

    ExecutionTask(

        id=2,

        description="Read matching email",

        agent="email",

        action="read",

        parameters={},

        depends_on=[1]
    ),

    ExecutionTask(

        id=3,

        description="Draft client reply",

        agent="email",

        action="draft_reply",

        parameters={
            "tone": "professional"
        },

        depends_on=[2]
    )
]


results = executor.execute(
    tasks
)


print("\nEXECUTION RESULTS")
print("=" * 60)


for task_id, result in results.items():

    print(
        f"Task {task_id}: "
        f"{result.status}"
    )

    print(
        "Output:",
        result.output
    )