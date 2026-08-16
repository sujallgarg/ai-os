from executor.task_running import (
    TaskRunner
)


class TaskExecutor:

    def __init__(
        self,
        agent_manager,
        log_service=None
    ):

        self.runner = TaskRunner(

            agent_manager,

            log_service
        )

    def execute(
        self,
        tasks,
        user_id="system"
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

                result = self.runner.run(

                    task,

                    user_id=user_id
                )

                results[
                    task.id
                ] = result

                pending.remove(
                    task
                )

                progress = True

                if result.status == "failed":

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