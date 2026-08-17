"""
Central Task Executor.

Responsibilities:

1. Find tasks whose dependencies are complete.
2. Select the highest-priority ready task.
3. Execute the task through TaskRunner.
4. Handle temporary failures with RetryManager.
5. Apply backoff between retries.
6. Pass exhausted failures to RecoveryManager.
7. Continue executing remaining tasks.
"""

from executor.task_running import (
    TaskRunner
)

from recovery.manager import (
    RecoveryManager
)

from priority.manager import (
    PriorityManager
)

from retry.manager import (
    RetryManager
)


class TaskExecutor:

    def __init__(
        self,
        agent_manager,
        log_service=None,
        recovery_manager=None,
        retry_manager=None,
        timeout_manager=None
    ):

        # --------------------------------
        # Task runner
        # --------------------------------

        self.runner = TaskRunner(

            agent_manager=agent_manager,

            log_service=log_service,

            timeout_manager=timeout_manager
        )

        # --------------------------------
        # Recovery manager
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

        # --------------------------------
        # Retry manager
        # --------------------------------

        self.retry_manager = (

            retry_manager

            or RetryManager()
        )

    # ============================================================
    # MAIN EXECUTION LOOP
    # ============================================================

    def execute(
        self,
        tasks,
        user_id="system"
    ):

        """
        Execute a collection of tasks.

        Execution order is determined by:

        1. Dependencies
        2. Priority
        3. Execution result
        4. Retry policy
        5. Recovery policy
        """

        # --------------------------------
        # Store completed task results
        # --------------------------------

        results = {}

        # --------------------------------
        # Pending task queue
        # --------------------------------

        pending = list(
            tasks
        )

        # --------------------------------
        # Main execution loop
        # --------------------------------

        while pending:

            print(
                "\n"
                + "=" * 70
            )

            print(
                "TASK EXECUTOR"
            )

            print(
                "=" * 70
            )

            print(
                "Pending tasks:",
                len(pending)
            )

            # --------------------------------
            # Find tasks that are ready
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
            # No task can currently run
            # --------------------------------

            if not ready_tasks:

                raise RuntimeError(
                    "No executable tasks available. "
                    "Check for unresolved or circular "
                    "task dependencies."
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
                getattr(
                    task,
                    "priority",
                    5
                )
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

            # ====================================================
            # SUCCESS
            # ====================================================

            if result.status == "completed":

                print(
                    f"\n✓ Task {task.id} completed."
                )

                # Store result

                results[
                    task.id
                ] = result

                # Remove from pending

                pending.remove(
                    task
                )

                # Reset retry counter because
                # task eventually succeeded.

                self.retry_manager.reset(
                    task.id
                )

                continue

            # ====================================================
            # FAILURE
            # ====================================================

            print(
                f"\n✗ Task {task.id} failed."
            )

            print(
                "Error:",
                result.error
            )

            error = (
                result.error
                or "Unknown execution error."
            )

            # ====================================================
            # RETRY DECISION
            # ====================================================

            retry_decision = (
                self.retry_manager.decide(

                    task_id=task.id,

                    error=error
                )
            )

            print(
                "\nRetry decision:"
            )

            print(
                "Should retry:",
                retry_decision.should_retry
            )

            print(
                "Attempt:",
                retry_decision.attempt
            )

            print(
                "Error type:",
                retry_decision.error_type
            )

            print(
                "Delay:",
                retry_decision.delay
            )

            print(
                "Reason:",
                retry_decision.reason
            )

            # ====================================================
            # RETRY
            # ====================================================

            if retry_decision.should_retry:

                print(
                    f"\n↻ Retrying task "
                    f"{task.id}..."
                )

                # Wait using exponential
                # backoff.

                self.retry_manager.wait(
                    retry_decision
                )

                # IMPORTANT:
                #
                # Do not remove the task
                # from pending.
                #
                # It will be selected again
                # on the next loop.

                continue

            # ====================================================
            # RETRIES EXHAUSTED / NON-RETRYABLE
            # ====================================================

            print(
                "\nRetries unavailable."
            )

            print(
                "Sending failure to "
                "RecoveryManager..."
            )

            recovery = (
                self.recovery.handle_failure(

                    task.id,

                    error
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

            # ====================================================
            # RECOVERY: RETRY
            # ====================================================
            #
            # This is included for compatibility
            # with your existing RecoveryManager.
            #
            # Normally RetryManager should handle
            # retryable failures first.
            # ====================================================

            if recovery.action == "RETRY":

                print(
                    f"\nRecovery requested "
                    f"another retry for task "
                    f"{task.id}."
                )

                continue

            # ====================================================
            # RECOVERY: ASK USER
            # ====================================================

            if recovery.action == "ASK_USER":

                print(
                    "\n⚠ User intervention "
                    "required."
                )

                results[
                    task.id
                ] = result

                pending.remove(
                    task
                )

                continue

            # ====================================================
            # RECOVERY: REPLAN
            # ====================================================

            if recovery.action == "REPLAN":

                print(
                    "\n↻ Task requires "
                    "replanning."
                )

                results[
                    task.id
                ] = result

                pending.remove(
                    task
                )

                # The future Planner /
                # Supervisor will replace
                # this task with a new plan.

                continue

            # ====================================================
            # RECOVERY: FAIL
            # ====================================================

            print(
                f"\n✗ Task {task.id} "
                "failed permanently."
            )

            results[
                task.id
            ] = result

            pending.remove(
                task
            )

        # ========================================================
        # EXECUTION COMPLETE
        # ========================================================

        print(
            "\n"
            + "=" * 70
        )

        print(
            "ALL TASKS PROCESSED"
        )

        print(
            "=" * 70
        )

        print(
            "Completed/processed:",
            len(results)
        )

        return results

    # ============================================================
    # DEPENDENCY CHECK
    # ============================================================

    def _dependencies_completed(
        self,
        task,
        results
    ):

        """
        Return True only when every dependency
        has completed successfully.
        """

        # --------------------------------
        # No dependencies
        # --------------------------------

        if not task.depends_on:

            return True

        # --------------------------------
        # Check every dependency
        # --------------------------------

        for dependency_id in (
            task.depends_on
        ):

            dependency_result = (
                results.get(
                    dependency_id
                )
            )

            # Dependency hasn't run yet.

            if dependency_result is None:

                return False

            # Dependency did not succeed.

            if (
                dependency_result.status
                != "completed"
            ):

                return False

        return True