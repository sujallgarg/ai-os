
from planner.multi_agent import (
    MultiAgentPlanner
)


class MockRegistry:

    def exists(
        self,
        agent_name
    ):

        return agent_name in [

            "email",

            "coding",

            "browser",

            "calendar",

            "file",

            "supervisor"
        ]


registry = MockRegistry()


planner = MultiAgentPlanner(
    registry
)


goal = (
    "Check my email, update my "
    "website and test it."
)


graph = planner.create_plan(
    goal
)


print(
    "\nMULTI-AGENT PLAN"
)

print(
    "=" * 70
)


for task_id, task in (
    graph.tasks.items()
):

    print(
        "\nTask:",
        task_id
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
        "Priority:",
        task.priority
    )

    print(
        "Dependencies:",
        task.depends_on
    )