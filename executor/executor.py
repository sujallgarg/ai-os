"""
Central Task Executor.

Responsibilities
----------------

1. Dependency-aware execution
2. Priority-aware execution
3. Timeout-aware execution through TaskRunner
4. Retry handling
5. Exponential backoff
6. Failure recovery
7. Dynamic agent capability matching
8. Supervisor monitoring
9. Dynamic task replanning
10. Agent handoff support
11. Human intervention support
12. Shared agent memory
13. Execution result tracking


Architecture
------------

                USER GOAL
                    |
                    v
                  PLANNER
                    |
                    v
                TASK GRAPH
                    |
                    v
           CAPABILITY MATCHER
                    |
                    v
               SUPERVISOR
                    |
                    v
                EXECUTOR
                    |
                    v
               TASK RUNNER
                    |
                    v
                  AGENT
                    |
             +------+------+
             |             |
             v             v
           TOOL         MEMORY
             |             |
             +------+------+
                    |
                    v
                 RESULT
                    |
          +---------+---------+
          |         |         |
        SUCCESS   RETRY    RECOVERY
                              |
                   +----------+----------+
                   |          |          |
                 REPLAN    HANDOFF     USER
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
        supervisor=None,
        capability_matcher=None,
        memory_manager=None
    ):
        """
        Initialize the central executor.

        Parameters
        ----------
        agent_manager:
            Manages available agents.

        log_service:
            Records execution logs.

        recovery_manager:
            Handles failures after retries.

        retry_manager:
            Controls retry decisions.

        timeout_manager:
            Controls execution timeouts.

        supervisor:
            Monitors the complete execution plan.

        capability_matcher:
            Dynamically selects agents.

        memory_manager:
            Shared memory available to agents.
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

        # ========================================================
        # CAPABILITY MATCHER
        # ========================================================

        self.capability_matcher = (
            capability_matcher
        )

        # ========================================================
        # SHARED MEMORY
        # ========================================================

        self.memory_manager = (
            memory_manager
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
        Execute the supplied task list.

        Tasks are processed according to:

            1. Dependencies
            2. Priority
            3. Agent capability
            4. Supervisor state
            5. Task execution
            6. Retry
            7. Recovery
            8. Replanning
        """

        # ========================================================
        # VALIDATION
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
        # RESULT STORAGE
        # ========================================================

        results = {}

        # ========================================================
        # PENDING TASK QUEUE
        # ========================================================

        pending = list(tasks)

        # ========================================================
        # SUPERVISOR START
        # ========================================================

        supervisor_goal = (
            goal
            or f"Execute {len(tasks)} tasks"
        )

        self.supervisor.start(
            goal=supervisor_goal,
            tasks=tasks
        )

        # ========================================================
        # EXECUTION HEADER
        # ========================================================

        print(
            "\n"
            + "=" * 70
        )

        print(
            "AI TASK EXECUTOR"
        )

        print(
            "=" * 70
        )

        print(
            "Goal:",
            supervisor_goal
        )

        print(
            "Tasks:",
            len(tasks)
        )

        # ========================================================
        # MAIN EXECUTION LOOP
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
                "Pending:",
                len(pending)
            )

            print(
                "Processed:",
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
                    "Possible causes:"
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

                decision = (
                    self.supervisor.decide(
                        pending
                    )
                )

                print(
                    "\n[Supervisor]"
                )

                print(
                    "Action:",
                    decision.action
                )

                print(
                    "Reason:",
                    decision.reason
                )

                raise RuntimeError(
                    "No executable tasks available."
                )

            # ====================================================
            # PRIORITY SORT
            # ====================================================

            ready_tasks = (
                self.priority_manager.sort(
                    ready_tasks
                )
            )

            # ====================================================
            # SELECT TASK
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

            print(
                "  Agent:",
                getattr(
                    task,
                    "agent",
                    None
                )
            )

            print(
                "  Required capabilities:",
                getattr(
                    task,
                    "required_capabilities",
                    []
                )
            )

            # ====================================================
            # RESOLVE AGENT
            # ====================================================

            agent_selection = (
                self._resolve_agent(task)
            )

            if not agent_selection["success"]:

                error = (
                    agent_selection["error"]
                )

                print(
                    "\n[Capability Matcher] "
                    "Could not resolve agent."
                )

                print(
                    "Reason:",
                    error
                )

                self.supervisor.task_failed(
                    task.id,
                    error
                )

                recovery = (
                    self._recover_task(
                        task,
                        error
                    )
                )

                if recovery.action == "RETRY":

                    print(
                        "\n↻ Retrying agent resolution."
                    )

                    retry_decision = (
                        self.retry_manager.decide(
                            task_id=task.id,
                            error=error
                        )
                    )

                    if retry_decision.should_retry:

                        self.retry_manager.wait(
                            retry_decision
                        )

                    continue

                if recovery.action == "REPLAN":

                    print(
                        "\n↻ Agent resolution "
                        "requires replanning."
                    )

                    replacement_tasks = (
                        self._dynamic_replan(
                            task,
                            error
                        )
                    )

                    results[
                        task.id
                    ] = self._failure_result(
                        task,
                        error
                    )

                    pending.remove(task)

                    pending.extend(
                        replacement_tasks
                    )

                    continue

                if recovery.action == "HANDOFF":

                    print(
                        "\n→ Agent handoff required."
                    )

                    results[
                        task.id
                    ] = self._failure_result(
                        task,
                        error
                    )

                    pending.remove(task)

                    continue

                if recovery.action == "ASK_USER":

                    print(
                        "\n⚠ User intervention required."
                    )

                    results[
                        task.id
                    ] = self._failure_result(
                        task,
                        error
                    )

                    pending.remove(task)

                    continue

                results[
                    task.id
                ] = self._failure_result(
                    task,
                    error
                )

                pending.remove(task)

                continue

            # ====================================================
            # ASSIGN SELECTED AGENT
            # ====================================================

            selected_agent = (
                agent_selection["agent"]
            )

            if selected_agent:

                task.agent = selected_agent

                print(
                    "\n[Capability Matcher]"
                )

                print(
                    "Selected agent:",
                    selected_agent
                )

            # ====================================================
            # ATTACH SHARED MEMORY
            # ====================================================

            self._attach_memory(
                task
            )

            # ====================================================
            # SUPERVISOR: TASK STARTED
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

                print(
                    "\n[Executor] "
                    "Unexpected exception:"
                )

                print(
                    str(error)
                )

                result = (
                    self._failure_result(
                        task,
                        str(error)
                    )
                )

            # ====================================================
            # SUCCESS
            # ====================================================

            if result.status == "completed":

                print(
                    f"\n✓ Task {task.id} completed."
                )

                # ----------------------------------------------
                # Supervisor
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
                # Store useful result in memory
                # ----------------------------------------------

                self._store_result_memory(
                    task,
                    result
                )

                # ----------------------------------------------
                # Remove task
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

            error = (
                result.error
                or "Unknown execution error."
            )

            print(
                f"\n✗ Task {task.id} failed."
            )

            print(
                "Error:",
                error
            )

            # ====================================================
            # SUPERVISOR FAILURE
            # ====================================================

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
                "  Retry:",
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

                self.retry_manager.wait(
                    retry_decision
                )

                continue

            # ====================================================
            # RECOVERY
            # ====================================================

            print(
                "\n[Executor]"
            )

            print(
                "Retry attempts exhausted."
            )

            print(
                "Starting recovery..."
            )

            recovery = (
                self._recover_task(
                    task,
                    error
                )
            )

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
                    f"retry for task {task.id}."
                )

                continue

            # ====================================================
            # RECOVERY → REPLAN
            # ====================================================

            if recovery.action == "REPLAN":

                print(
                    "\n↻ Dynamic replanning required."
                )

                replacement_tasks = (
                    self._dynamic_replan(
                        task,
                        error
                    )
                )

                # ----------------------------------------------
                # Save failed result
                # ----------------------------------------------

                results[
                    task.id
                ] = result

                # ----------------------------------------------
                # Remove failed task
                # ----------------------------------------------

                pending.remove(
                    task
                )

                # ----------------------------------------------
                # Add replacement tasks
                # ----------------------------------------------

                pending.extend(
                    replacement_tasks
                )

                print(
                    "\n[Replanner] Added",
                    len(replacement_tasks),
                    "replacement tasks."
                )

                continue

            # ====================================================
            # RECOVERY → HANDOFF
            # ====================================================

            if recovery.action == "HANDOFF":

                print(
                    "\n→ Agent handoff required."
                )

                results[
                    task.id
                ] = result

                pending.remove(
                    task
                )

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

                results[
                    task.id
                ] = result

                pending.remove(
                    task
                )

                continue

            # ====================================================
            # PERMANENT FAILURE
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
        # FINAL SUPERVISOR CHECK
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
            "Supervisor action:",
            final_decision.action
        )

        print(
            "Supervisor reason:",
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
    # AGENT RESOLUTION
    # ============================================================

    def _resolve_agent(
        self,
        task
    ):
        """
        Resolve the correct agent.

        Priority:

        1. Explicit task.agent
        2. Required capabilities
        3. Capability matcher
        """

        # --------------------------------------------------------
        # Explicit agent
        # --------------------------------------------------------

        existing_agent = getattr(
            task,
            "agent",
            None
        )

        if existing_agent:

            return {
                "success": True,
                "agent": existing_agent
            }

        # --------------------------------------------------------
        # Required capabilities
        # --------------------------------------------------------

        required_capabilities = getattr(
            task,
            "required_capabilities",
            []
        )

        if not required_capabilities:

            return {
                "success": False,
                "agent": None,
                "error": (
                    f"Task {task.id} "
                    "has no agent and no "
                    "required capabilities."
                )
            }

        # --------------------------------------------------------
        # Matcher unavailable
        # --------------------------------------------------------

        if self.capability_matcher is None:

            return {
                "success": False,
                "agent": None,
                "error": (
                    "CapabilityMatcher "
                    "is not configured."
                )
            }

        # --------------------------------------------------------
        # Match
        # --------------------------------------------------------

        try:

            agent = (
                self.capability_matcher
                .find_best_agent(
                    required_capabilities
                )
            )

        except Exception as error:

            return {
                "success": False,
                "agent": None,
                "error": (
                    "Capability matching "
                    f"failed: {error}"
                )
            }

        # --------------------------------------------------------
        # No match
        # --------------------------------------------------------

        if agent is None:

            return {
                "success": False,
                "agent": None,
                "error": (
                    "No available agent "
                    "supports: "
                    + ", ".join(
                        required_capabilities
                    )
                )
            }

        # --------------------------------------------------------
        # Agent name
        # --------------------------------------------------------

        agent_name = getattr(
            agent,
            "name",
            None
        )

        if not agent_name:

            return {
                "success": False,
                "agent": None,
                "error": (
                    "CapabilityMatcher "
                    "returned an invalid agent."
                )
            }

        return {
            "success": True,
            "agent": agent_name
        }

    # ============================================================
    # MEMORY ATTACHMENT
    # ============================================================

    def _attach_memory(
        self,
        task
    ):
        """
        Attach a SharedMemory interface to the task.

        The actual Agent should use this interface
        when executing the task.
        """

        if self.memory_manager is None:

            return

        agent_id = getattr(
            task,
            "agent",
            None
        )

        if not agent_id:

            return

        try:

            from memory.shared import (
                SharedMemory
            )

            task.memory = SharedMemory(
                self.memory_manager,
                agent_id
            )

            print(
                "[Memory] Shared memory "
                f"attached to {agent_id}"
            )

        except ImportError:

            print(
                "[Memory] SharedMemory "
                "module unavailable."
            )

    # ============================================================
    # STORE RESULT IN MEMORY
    # ============================================================

    def _store_result_memory(
        self,
        task,
        result
    ):
        """
        Store a lightweight task result
        in shared memory.

        Do not store raw credentials,
        secrets, or sensitive data here.
        """

        if self.memory_manager is None:

            return

        agent_id = getattr(
            task,
            "agent",
            None
        )

        if not agent_id:

            return

        try:

            self.memory_manager.remember(

                key=f"task.{task.id}.result",

                value={
                    "status": "completed",
                    "task": task.description
                },

                agent_id=agent_id,

                memory_type="result",

                importance=5,

                metadata={
                    "task_id": task.id
                }
            )

            print(
                "[Memory] Task result stored."
            )

        except Exception as error:

            print(
                "[Memory] Could not store result:",
                error
            )

    # ============================================================
    # DYNAMIC REPLANNING
    # ============================================================

    def _dynamic_replan(
        self,
        task,
        error
    ):
        """
        Ask the Supervisor/Replanner to generate
        replacement tasks.
        """

        try:

            graph = (
                self.supervisor.replan_task(
                    task,
                    error
                )
            )

            if graph is None:

                return []

            replacement_tasks = list(
                graph.tasks.values()
            )

            for replacement in (
                replacement_tasks
            ):

                print(
                    "\n[Replanner] New task:"
                )

                print(
                    "  ID:",
                    replacement.id
                )

                print(
                    "  Description:",
                    replacement.description
                )

                print(
                    "  Action:",
                    replacement.action
                )

                print(
                    "  Capabilities:",
                    getattr(
                        replacement,
                        "required_capabilities",
                        []
                    )
                )

                print(
                    "  Dependencies:",
                    getattr(
                        replacement,
                        "depends_on",
                        []
                    )
                )

            return replacement_tasks

        except Exception as error:

            print(
                "\n[Replanner] Failed:"
            )

            print(
                str(error)
            )

            return []

    # ============================================================
    # RECOVERY
    # ============================================================

    def _recover_task(
        self,
        task,
        error
    ):
        """
        Call RecoveryManager.

        Supports both the current API and
        older versions.
        """

        try:

            return (
                self.recovery.handle_failure(

                    task_id=task.id,

                    error=error,

                    task=task
                )
            )

        except TypeError:

            return (
                self.recovery.handle_failure(

                    task.id,

                    error
                )
            )

    # ============================================================
    # DEPENDENCY CHECK
    # ============================================================

    def _dependencies_completed(
        self,
        task,
        results
    ):
        """
        Return True when all dependencies
        have completed successfully.
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
        # Check dependencies
        # --------------------------------------------------------

        for dependency_id in dependencies:

            dependency_result = (
                results.get(
                    dependency_id
                )
            )

            if dependency_result is None:

                return False

            if (
                dependency_result.status
                != "completed"
            ):

                return False

        return True

    # ============================================================
    # FAILURE RESULT
    # ============================================================

    def _failure_result(
        self,
        task,
        error
    ):
        """
        Create a failure result for executor-level errors.
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