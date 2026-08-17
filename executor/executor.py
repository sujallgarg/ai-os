"""
Central Task Executor.

Responsibilities:

1. Find tasks whose dependencies are complete.
2. Select the highest-priority ready task.
3. Execute the task through TaskRunner.
4. Detect task failures.
5. Retry temporary failures.
6. Apply exponential backoff.
7. Pass exhausted failures to RecoveryManager.
8. Support replanning.
9. Support user intervention.
10. Continue processing remaining tasks.
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

        # ========================================================
        # TASK RUNNER
        # ========================================================

        self.runner = TaskRunner(

            agent_manager=agent_manager,

            log_service=log_service,

            timeout_manager=timeout_manager
        )

        # ========================================================
        # RECOVERY MANAGER
        # ========================================================

        self.recovery = (

            recovery_manager

            or RecoveryManager()
        )

        # ========================================================
        # PRIORITY MANAGER
        # ========================================================

        self.priority_manager = (

            PriorityManager()
        )

        # ========================================================
        # RETRY MANAGER
        # ========================================================

        self.retry_manager = (

            retry_manager

            or RetryManager()
        )

    # ============================================================
    # MAIN EXECUTION METHOD
    # ============================================================

    def execute(
        self,
        tasks,
        user_id="system"
    ):

        """
        Execute a list of tasks.

        Execution order is determined by:

        1. Dependencies
        2. Priority
        3. Agent execution
        4. Retry policy
        5. Recovery policy
        """

        # --------------------------------------------------------
        # Results of processed tasks
        # --------------------------------------------------------

        results = {}

        # --------------------------------------------------------
        # Pending task queue
        # --------------------------------------------------------

        pending = list(
            tasks
        )

        # ========================================================
        # MAIN LOOP
        # ========================================================

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

            # ====================================================
            # FIND READY TASKS
            # ====================================================

            ready_tasks = [

                task

                for task in pending

                if self._dependencies_completed(
                    task,
                    results
                )
            ]

            # ====================================================
            # NO READY TASK
            # ====================================================

            if not ready_tasks:

                raise RuntimeError(
                    "No executable tasks available. "
                    "Possible circular or unresolved "
                    "dependencies."
                )

            # ====================================================
            # SORT BY PRIORITY
            # ====================================================

            ready_tasks = (
                self.priority_manager.sort(
                    ready_tasks
                )
            )

            # ====================================================
            # SELECT HIGHEST PRIORITY TASK
            # ====================================================

            task = ready_tasks[0]

            print(
                "\nSelected task:"
            )

            print(
                "--------------------------------"
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

            print(
                "--------------------------------"
            )

            # ====================================================
            # EXECUTE TASK
            # ====================================================

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

                # Remove completed task

                pending.remove(
                    task
                )

                # Reset retry counter

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

            error = (

                result.error

                or "Unknown execution error."
            )

            print(
                "Error:",
                error
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
                "--------------------------------"
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

            print(
                "--------------------------------"
            )

            # ====================================================
            # RETRY
            # ====================================================

            if retry_decision.should_retry:

                print(
                    f"\n↻ Retrying task "
                    f"{task.id}..."
                )

                # Exponential backoff

                self.retry_manager.wait(
                    retry_decision
                )

                # IMPORTANT:
                #
                # Do not remove the task from
                # pending.
                #
                # The task will be selected
                # again on the next iteration.

                continue

            # ====================================================
            # RETRIES EXHAUSTED
            # ====================================================

            print(
                "\nRetry unavailable."
            )

            print(
                "Passing failure to "
                "RecoveryManager..."
            )

            # ====================================================
            # FAILURE RECOVERY
            # ====================================================

            recovery = (

                self.recovery.handle_failure(

                    task_id=task.id,

                    error=error,

                    task=task
                )
            )

            print(
                "\nRecovery decision:"
            )

            print(
                "--------------------------------"
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

            print(
                "--------------------------------"
            )

            # ====================================================
            # RECOVERY → RETRY
            # ====================================================

            if recovery.action == "RETRY":

                print(
                    f"\n↻ Recovery requested "
                    f"another attempt for "
                    f"task {task.id}."
                )

                continue

            # ====================================================
            # RECOVERY → REPLAN
            # ====================================================

            if recovery.action == "REPLAN":

                print(
                    "\n↻ Replanning required."
                )

                print(
                    "Replan request:"
                )

                print(
                    recovery.replan_request
                )

                # Store failed result

                results[
                    task.id
                ] = result

                # Remove old task

                pending.remove(
                    task
                )

                # IMPORTANT:
                #
                # The future Supervisor/Planner
                # will insert replacement tasks.
                #
                # Step 69 will connect this
                # directly to the Planner.

                continue

            # ====================================================
            # RECOVERY → HANDOFF
            # ====================================================

            if recovery.action == "HANDOFF":

                print(
                    "\n→ Agent handoff required."
                )

                # Store current result

                results[
                    task.id
                ] = result

                pending.remove(
                    task
                )

                # The future multi-agent
                # recovery system will create
                # the replacement handoff task.

                continue

            # ====================================================
            # RECOVERY → ASK USER
            # ====================================================

            if recovery.action == "ASK_USER":

                print(
                    "\n⚠ User intervention "
                    "required."
                )

                print(
                    "Task:",
                    task.description
                )

                results[
                    task.id
                ] = result

                pending.remove(
                    task
                )

                continue

            # ====================================================
            # RECOVERY → FAIL
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
        # EXECUTION FINISHED
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
            "Processed tasks:",
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
        Check whether every dependency of a task
        has completed successfully.
        """

        # --------------------------------------------------------
        # No dependencies
        # --------------------------------------------------------

        if not task.depends_on:

            return True

        # --------------------------------------------------------
        # Check dependencies
        # --------------------------------------------------------

        for dependency_id in (
            task.depends_on
        ):

            dependency_result = (

                results.get(
                    dependency_id
                )
            )

            # ----------------------------------------------------
            # Dependency has not executed
            # ----------------------------------------------------

            if dependency_result is None:

                return False

            # ----------------------------------------------------
            # Dependency failed
            # ----------------------------------------------------

            if (
                dependency_result.status
                != "completed"
            ):

                return False

        # --------------------------------------------------------
        # All dependencies completed
        # --------------------------------------------------------

        return True