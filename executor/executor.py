"""
Task Executor.

Executes decomposed tasks while respecting
dependencies.
"""

from executor.task_running import (
    TaskRunner
)


class TaskExecutor:

    def __init__(
        self,
        agent_manager
    ):

        self.runner = TaskRunner(
            agent_manager
        )

    def execute(
        self,
        tasks
    ):

        results = {}

        pending = list(
            tasks
        )

        while pending:

            progress = False

            for task in pending:

                if not self._dependencies_completed(
                    task,
                    results
                ):

                    continue

                print(
                    f"\n[Executor] "
                    f"Executing task {task.id}"
                )

                result = self.runner.run(
                    task
                )

                results[
                    task.id
                ] = result

                pending.remove(
                    task
                )

                progress = True

                if result.status == "failed":

                    print(
                        f"[Executor] "
                        f"Stopping because task "
                        f"{task.id} failed."
                    )

                    return results

                break

            if not progress:

                raise RuntimeError(
                    "Unable to resolve task "
                    "dependencies."
                )

        return results

    def _dependencies_completed(
        self,
        task,
        results
    ):

        for dependency_id in (
            task.depends_on
        ):

            dependency = results.get(
                dependency_id
            )

            if dependency is None:

                return False

            if dependency.status != "completed":

                return False

        return True