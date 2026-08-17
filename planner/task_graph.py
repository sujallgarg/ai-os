"""
Task dependency graph.

Represents tasks and their dependencies
inside a multi-agent execution plan.
"""


class TaskGraph:

    def __init__(self):

        self.tasks = {}

        self.dependencies = {}

    def add_task(
        self,
        task
    ):

        self.tasks[
            task.id
        ] = task

        self.dependencies[
            task.id
        ] = list(
            getattr(
                task,
                "depends_on",
                []
            )
        )

    def get_task(
        self,
        task_id
    ):

        return self.tasks.get(
            task_id
        )

    def get_dependencies(
        self,
        task_id
    ):

        return self.dependencies.get(
            task_id,
            []
        )

    def get_ready_tasks(
        self,
        completed_ids
    ):

        ready = []

        for task_id, task in (
            self.tasks.items()
        ):

            dependencies = (
                self.dependencies.get(
                    task_id,
                    []
                )
            )

            if task_id in completed_ids:

                continue

            if all(
                dependency in completed_ids
                for dependency in dependencies
            ):

                ready.append(
                    task
                )

        return ready

    def is_complete(
        self,
        completed_ids
    ):

        return len(
            completed_ids
        ) == len(
            self.tasks
        )

    def validate(self):

        # Check that every dependency
        # actually exists.

        for task_id, dependencies in (
            self.dependencies.items()
        ):

            for dependency_id in dependencies:

                if dependency_id not in self.tasks:

                    raise ValueError(

                        f"Task {task_id} "
                        f"depends on unknown "
                        f"task {dependency_id}"
                    )

        return True