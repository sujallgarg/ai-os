from executor.task_runner import (
    TaskRunner
)

from recovery.manager import (
    RecoveryManager
)


class TaskExecutor:

    def __init__(
        self,
        agent_manager,
        log_service=None,
        recovery_manager=None
    ):

        self.runner = TaskRunner(

            agent_manager,

            log_service
        )

        self.recovery = (
            recovery_manager
            or RecoveryManager()
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

                # --------------------------------
                # Successful task
                # --------------------------------

                if result.status == "completed":

                    results[
                        task.id
                    ] = result

                    pending.remove(
                        task
                    )

                    progress = True

                    break

                # --------------------------------
                # Failed task
                # --------------------------------

                recovery = (
                    self.recovery.handle_failure(

                        task.id,

                        result.error
                    )
                )

                print(
                    f"[Recovery] "
                    f"Task {task.id}: "
                    f"{recovery.action}"
                )

                # --------------------------------
                # Retry
                # --------------------------------

                if recovery.action == "RETRY":

                    continue

                # --------------------------------
                # Ask user
                # --------------------------------

                if recovery.action == "ASK_USER":

                    results[
                        task.id
                    ] = result

                    pending.remove(
                        task
                    )

                    progress = True

                    print(
                        "[Executor] "
                        "User intervention required."
                    )

                    break

                # --------------------------------
                # Permanent failure
                # --------------------------------

                results[
                    task.id
                ] = result

                pending.remove(
                    task
                )

                progress = True

                print(
                    f"[Executor] "
                    f"Task {task.id} failed permanently."
                )

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