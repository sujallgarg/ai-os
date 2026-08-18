from planner.replanner import (
    DynamicReplanner
)


class MockTask:

    def __init__(self):

        self.id = 1

        self.description = (
            "Build the website"
        )

        self.agent = "coding"

        self.action = "build"

        self.parameters = {}


replanner = DynamicReplanner()


task = MockTask()


graph = replanner.replan(

    original_task=task,

    error=(
        "Build failed because "
        "of a missing dependency."
    )
)


print(
    "\nDYNAMIC REPLAN"
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
        "Action:",
        task.action
    )

    print(
        "Capabilities:",
        task.required_capabilities
    )

    print(
        "Dependencies:",
        task.depends_on
    )

    print(
        "Priority:",
        task.priority
    )