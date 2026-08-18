"""
Central Task Executor.

Responsibilities:

1. Find tasks whose dependencies are complete.
2. Select the highest-priority ready task.
3. Notify the Supervisor when tasks start.
4. Execute tasks through TaskRunner.
5. Handle successful tasks.
6. Handle temporary failures with RetryManager.
7. Apply retry backoff.
8. Pass exhausted failures to RecoveryManager.
9. Support replanning.
10. Support agent handoffs.
11. Support user intervention.
12. Notify the Supervisor about task state.
13. Continue until all executable tasks are processed.
"""

from executor.task_running import TaskRunner

from recovery.manager import RecoveryManager

from priority.manager import PriorityManager

from retry.manager import RetryManager

from supervisor.supervisor import SupervisorAgent


class TaskExecutor:

    def __init__(
        self,
        agent_manager,
        log_service=None,
        recovery_manager=None,
        retry_manager=None,
        timeout_manager=None,
        supervisor=None
    ):
        """
        Initialize the central task executor.

        Parameters
        ----------
        agent_manager:
            Manages and executes AI agents.

        log_service:
            Records task execution logs.

        recovery_manager:
            Handles failures after retries are exhausted.

        retry_manager:
            Handles retry decisions and backoff.

        timeout_manager:
            Controls maximum execution time.

        supervisor:
            Monitors the overall execution plan.
        """

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

        # ========================================================
        # SUPERVISOR
        # ========================================================

        self.supervisor = (
            supervisor
            or SupervisorAgent(
                recovery_manager=self.recovery
            )
        )

    # ============================================================
    # MAIN EXECUTION METHOD
    # ============================================================

    def execute(
        self,
        tasks,
        user_id="system",
        goal=None
    ):
        """
        Execute a list of tasks.

        Execution order:

            Dependencies
                  ↓
             Ready tasks
                  ↓
               Priority
                  ↓
             TaskRunner
                  ↓
               Agent
                  ↓
              Success/Error
                  ↓
             Retry/Recovery

        Returns
        -------
        dict
            Mapping of task IDs to task results.
        """

        # ========================================================
        # VALIDATE INPUT
        # ========================================================

        if tasks is None:

            raise ValueError(
                "tasks cannot be None."
            )

        tasks = list(tasks)

        if not tasks:

            print(
                "[Executor] No tasks to execute."
            )

            return {}

        # ========================================================
        # EXECUTION STATE
        # ========================================================

        results = {}

        # Copy tasks so the original list isn't modified.

        pending = list(tasks)

        # ========================================================
        # START SUPERVISOR
        # ========================================================

        supervisor_goal = (
            goal
            or f"Execute {len(tasks)} tasks"
        )

        self.supervisor.start(
            goal=supervisor_goal,
            tasks=tasks
        )

        print(
            "\n"
            + "=" * 70
        )

        print(
            "STARTING TASK EXECUTION"
        )

        print(
            "=" * 70
        )

        print(
            "Goal:",
            supervisor_goal
        )

        print(
            "Total tasks:",
            len(tasks)
        )

        # ========================================================
        # MAIN LOOP
        # ========================================================

        while pending:

            print(
                "\n"
                + "-" * 70
            )

            print(
                "EXECUTOR LOOP"
            )

            print(
                "-" * 70
            )

            print(
                "Pending tasks:",
                len(pending)
            )

            print(
                "Completed tasks:",
                len(results)
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

                print(
                    "\n[Executor] No ready tasks."
                )

                print(
                    "[Executor] Possible causes:"
                )

                print(
                    "  - unresolved dependency"
                )

                print(
                    "  - circular dependency"
                )

                print(
                    "  - failed dependency"
                )

                # Tell Supervisor the execution
                # is blocked.

                decision = self.supervisor.decide(
                    pending
                )

                print(
                    "[Supervisor] Action:",
                    decision.action
                )

                print(
                    "[Supervisor] Reason:",
                    decision.reason
                )

                # If the supervisor cannot resolve
                # the situation yet, stop rather than
                # creating an infinite loop.

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
                "  ID:",
                task.id
            )

            print(
                "  Description:",
                task.description
            )

            print(
                "  Agent:",
                task.agent
            )

            print(
                "  Action:",
                task.action
            )

            print(
                "  Priority:",
                getattr(
                    task,
                    "priority",
                    5
                )
            )

            print(
                "  Dependencies:",
                getattr(
                    task,
                    "depends_on",
                    []
                )
            )

            # ====================================================
            # NOTIFY SUPERVISOR
            # ====================================================

            self.supervisor.task_started(
                task.id
            )

            # ====================================================
            # EXECUTE TASK
            # ====================================================

            try:

                result = self.runner.run(
                    task,
                    user_id=user_id
                )

            except Exception as error:

                # Protect the main executor from an
                # unexpected exception escaping TaskRunner.

                print(
                    "\n[Executor] Unexpected exception:"
                )

                print(
                    str(error)
                )

                # Convert the exception into a
                # failure-like result.

                result = self._create_failure_result(
                    task,
                    str(error)
                )

            # ====================================================
            # SUCCESS
            # ====================================================

            if result.status == "completed":

                print(
                    f"\n✓ Task {task.id} completed."
                )

                # ----------------------------------------------
                # Notify Supervisor
                # ----------------------------------------------

                self.supervisor.task_completed(
                    task.id,
                    result
                )

                # ----------------------------------------------
                # Store result
                # ----------------------------------------------

                results[
                    task.id
                ] = result

                # ----------------------------------------------
                # Remove task from pending
                # ----------------------------------------------

                pending.remove(
                    task
                )

                # ----------------------------------------------
                # Reset retry counter
                # ----------------------------------------------

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

            # ----------------------------------------------
            # Notify Supervisor
            # ----------------------------------------------

            self.supervisor.task_failed(
                task.id,
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
                "  Should retry:",
                retry_decision.should_retry
            )

            print(
                "  Attempt:",
                retry_decision.attempt
            )

            print(
                "  Error type:",
                retry_decision.error_type
            )

            print(
                "  Delay:",
                retry_decision.delay
            )

            print(
                "  Reason:",
                retry_decision.reason
            )

            # ====================================================
            # RETRY
            # ====================================================

            if retry_decision.should_retry:

                print(
                    f"\n↻ Retrying task {task.id}..."
                )

                # Exponential backoff.

                self.retry_manager.wait(
                    retry_decision
                )

                # IMPORTANT:
                #
                # Do not remove the task from
                # pending.
                #
                # It will be selected again.

                continue

            # ====================================================
            # RETRIES EXHAUSTED
            # ====================================================

            print(
                "\n[Executor] Retry unavailable."
            )

            print(
                "[Executor] Passing failure "
                "to RecoveryManager..."
            )

            # ====================================================
            # FAILURE RECOVERY
            # ====================================================

            try:

                recovery = (
                    self.recovery.handle_failure(

                        task_id=task.id,

                        error=error,

                        task=task
                    )
                )

            except TypeError:

                # Compatibility with an older
                # RecoveryManager implementation
                # that doesn't accept task=.

                recovery = (
                    self.recovery.handle_failure(

                        task.id,

                        error
                    )
                )

            # ====================================================
            # PRINT RECOVERY DECISION
            # ====================================================

            print(
                "\nRecovery decision:"
            )

            print(
                "  Action:",
                recovery.action
            )

            print(
                "  Reason:",
                recovery.reason
            )

            print(
                "  Retry count:",
                recovery.retry_count
            )

            # ====================================================
            # RECOVERY → RETRY
            # ====================================================

            if recovery.action == "RETRY":

                print(
                    f"\n↻ Recovery requested "
                    f"another attempt for task "
                    f"{task.id}."
                )

                # Do not remove from pending.

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

                # Store failed result.

                results[
                    task.id
                ] = result

                # Remove failed task.

                pending.remove(
                    task
                )

                # ------------------------------------------------
                # Step 69/70:
                #
                # The Planner/Supervisor will eventually
                # create replacement tasks here.
                #
                # Step 72 will connect this directly
                # to dynamic replanning.
                # ------------------------------------------------

                continue

            # ====================================================
            # RECOVERY → HANDOFF
            # ====================================================

            if recovery.action == "HANDOFF":

                print(
                    "\n→ Agent handoff required."
                )

                # Store current failure.

                results[
                    task.id
                ] = result

                # Remove current task.

                pending.remove(
                    task
                )

                # ------------------------------------------------
                # The Capability Matching system will
                # eventually create a replacement task
                # for another agent.
                # ------------------------------------------------

                continue

            # ====================================================
            # RECOVERY → ASK USER
            # ====================================================

            if recovery.action == "ASK_USER":

                print(
                    "\n⚠ User intervention required."
                )

                print(
                    "Task:",
                    task.description
                )

                # Store result.

                results[
                    task.id
                ] = result

                # Remove task from active queue.

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
        # FINAL SUPERVISOR DECISION
        # ========================================================

        final_decision = (
            self.supervisor.decide(
                pending
            )
        )

        print(
            "\n"
            + "=" * 70
        )

        print(
            "EXECUTION FINISHED"
        )

        print(
            "=" * 70
        )

        print(
            "Supervisor:",
            final_decision.action
        )

        print(
            "Reason:",
            final_decision.reason
        )

        print(
            "Processed tasks:",
            len(results)
        )

        # ========================================================
        # RETURN RESULTS
        # ========================================================

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

        dependencies = getattr(
            task,
            "depends_on",
            []
        )

        # --------------------------------------------------------
        # No dependencies
        # --------------------------------------------------------

        if not dependencies:

            return True

        # --------------------------------------------------------
        # Check every dependency
        # --------------------------------------------------------

        for dependency_id in dependencies:

            dependency_result = (
                results.get(
                    dependency_id
                )
            )

            # ----------------------------------------------------
            # Dependency has not run yet.
            # ----------------------------------------------------

            if dependency_result is None:

                return False

            # ----------------------------------------------------
            # Dependency failed.
            # ----------------------------------------------------

            if (
                dependency_result.status
                != "completed"
            ):

                return False

        # --------------------------------------------------------
        # Every dependency succeeded.
        # --------------------------------------------------------

        return True

    # ============================================================
    # FAILURE RESULT
    # ============================================================

    def _create_failure_result(
        self,
        task,
        error
    ):
        """
        Create a TaskResult when TaskRunner itself
        unexpectedly raises an exception.
        """

        try:

            from executor.result import (
                TaskResult
            )

            return TaskResult(

                task_id=task.id,

                status="failed",

                error=error
            )

        except ImportError:

            # Fallback object if your current
            # result module has a different structure.

            class FailureResult:

                def __init__(
                    self,
                    task_id,
                    error
                ):

                    self.task_id = (
                        task_id
                    )

                    self.status = (
                        "failed"
                    )

                    self.error = (
                        error
                    )

            return FailureResult(
                task.id,
                error
            )