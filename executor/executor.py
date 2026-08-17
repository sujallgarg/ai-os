"""
Task Executor.

Executes tasks while respecting:

1. Dependencies
2. Task priority
3. Agent availability
4. Error recovery
5. Execution logging
"""

from executor.task_runner import (
    TaskRunner
)

from recovery.manager import (
    RecoveryManager
)

from priority.manager import (
    PriorityManager
)


class TaskExecutor:

    def __init__(
        self,
        agent_manager,
        log_service=None,
        recovery_manager=None
    ):

        # --------------------------------
        # Agent task runner
        # --------------------------------

        self.runner = TaskRunner(

            agent_manager,

            log_service
        )

        # --------------------------------
        # Error recovery
        # --------------------------------

        self.recovery = (

            recovery_manager

            or RecoveryManager()
        )

        # --------------------------------
        # Priority manager
        # --------------------------------

        self.priority_manager = (
            PriorityManager()
        )

    def execute(
        self,
        tasks,
        user_id="system"
    ):

        """
        Execute a collection of tasks.

        The executor:

        1. Finds tasks whose dependencies
           are completed.
        2. Sorts ready tasks by priority.
        3. Executes the highest-priority task.
        4. Handles failures.
        5. Continues until all tasks finish.
        """

        # --------------------------------
        # Store execution results
        # --------------------------------

        results = {}

        # --------------------------------
        # Copy tasks into pending queue
        # --------------------------------

        pending = list(
            tasks
        )

        # --------------------------------
        # Continue while tasks remain
        # --------------------------------

        while pending:

            print(
                "\n================================"
            )

            print(
                "EXECUTOR"
            )

            print(
                "Pending tasks:",
                len(pending)
            )

            print(
                "================================"
            )

            # --------------------------------
            # Find tasks whose dependencies
            # are already completed
            # --------------------------------

            ready_tasks = [

                task

                for task in pending

                if self._dependencies_completed(
                    task,
                    results
                )
            ]

            # --------------------------------
            # Make sure at least one task
            # can be executed
            # --------------------------------

            if not ready_tasks:

                raise RuntimeError(
                    "No executable tasks available. "
                    "There may be unresolved "
                    "dependencies."
                )

            # --------------------------------
            # Sort ready tasks by priority
            # --------------------------------

            ready_tasks = (
                self.priority_manager.sort(
                    ready_tasks
                )
            )

            # --------------------------------
            # Select highest-priority task
            # --------------------------------

            task = ready_tasks[0]

            print(
                "\nSelected task:"
            )

            print(
                "ID:",
                task.id
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

            # --------------------------------
            # Execute task
            # --------------------------------

            result = self.runner.run(

                task,

                user_id=user_id
            )

            # --------------------------------
            # SUCCESS
            # --------------------------------

            if result.status == "completed":

                print(
                    f"\nTask {task.id} completed."
                )

                results[
                    task.id
                ] = result

                pending.remove(
                    task
                )

                continue

            # --------------------------------
            # FAILURE
            # --------------------------------

            print(
                f"\nTask {task.id} failed."
            )

            print(
                "Error:",
                result.error
            )

            # --------------------------------
            # Ask recovery manager
            # what to do
            # --------------------------------

            recovery = (
                self.recovery.handle_failure(

                    task.id,

                    result.error
                )
            )

            print(
                "\nRecovery decision:"
            )

            print(
                "Action:",
                recovery.action
            )

            print(
                "Reason:",
                recovery.reason
            )

            print(
                "Retry count:",
                recovery.retry_count
            )

            # --------------------------------
            # RETRY
            # --------------------------------

            if recovery.action == "RETRY":

                print(
                    f"\nRetrying task "
                    f"{task.id}..."
                )

                # Don't remove the task
                # from pending.
                #
                # It will be selected again.

                continue

            # --------------------------------
            # ASK USER
            # --------------------------------

            if recovery.action == "ASK_USER":

                print(
                    "\nUser intervention "
                    "required."
                )

                results[
                    task.id
                ] = result

                pending.remove(
                    task
                )

                continue

            # --------------------------------
            # PERMANENT FAILURE
            # --------------------------------

            print(
                f"\nTask {task.id} "
                "failed permanently."
            )

            results[
                task.id
            ] = result

            pending.remove(
                task
            )

        # --------------------------------
        # All tasks completed
        # --------------------------------

        print(
            "\n================================"
        )

        print(
            "EXECUTION FINISHED"
        )

        print(
            "================================"
        )

        return results

    def _dependencies_completed(
        self,
        task,
        results
    ):

        """
        Check whether all dependencies
        for a task have completed successfully.
        """

        # --------------------------------
        # Task has no dependencies
        # --------------------------------

        if not task.depends_on:

            return True

        # --------------------------------
        # Check every dependency
        # --------------------------------

        for dependency_id in (
            task.depends_on
        ):

            dependency = results.get(
                dependency_id
            )

            # Dependency hasn't executed yet
            if dependency is None:

                return False

            # Dependency failed
            if dependency.status != "completed":

                return False

        # --------------------------------
        # Every dependency succeeded
        # --------------------------------

        return True