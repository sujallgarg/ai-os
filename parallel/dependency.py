"""
Determines which tasks can safely run in parallel.
"""


def find_ready_tasks(
    tasks,
    completed_ids
):

    ready = []

    for task in tasks:

        dependencies = getattr(
            task,
            "depends_on",
            []
        )

        if all(
            dependency in completed_ids
            for dependency in dependencies
        ):

            ready.append(
                task
            )

    return ready