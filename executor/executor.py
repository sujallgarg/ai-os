"""
Central Task Executor.

Current capabilities:

1. Dependency-aware execution
2. Priority-aware execution
3. Timeout-aware execution through TaskRunner
4. Retry handling
5. Exponential backoff
6. Failure recovery
7. Dynamic replanning
8. Agent handoff support
9. Human intervention support
10. Supervisor monitoring
11. Dynamic agent capability matching

Architecture:

    User Goal
        ↓
    Planner
        ↓
    Task Graph
        ↓
    Capability Matcher
        ↓
    Supervisor
        ↓
    Executor
        ↓
    TaskRunner
        ↓
    Agent
        ↓
    Tool
        ↓
    Result
        ↓
    Retry / Recovery / Replan
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
        capability_matcher=None
    ):
        """
        Initialize the central task executor.

        Parameters
        ----------
        agent_manager:
            Manages available agents and executes them.

        log_service:
            Records task execution history.

        recovery_manager:
            Handles failures after retry attempts.

        retry_manager:
            Handles retry decisions and backoff.

        timeout_manager:
            Controls execution timeouts.

        supervisor:
            Monitors the overall execution plan.

        capability_matcher:
            Dynamically selects an agent based on
            required capabilities.
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

                recovery_manager=
                    self.recovery
            )
        )

        # ========================================================
        # CAPABILITY MATCHER
        # ========================================================

        self.capability_matcher = (
            capability_matcher
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
        Execute a collection of tasks.

        Flow:

            Tasks
              ↓
            Dependencies
              ↓
            Ready Tasks
              ↓
            Priority
              ↓
            Capability Matching
              ↓
            Supervisor
              ↓
            TaskRunner
              ↓
            Agent
              ↓
            Success / Failure
              ↓
            Retry / Recovery

        Returns
        -------
        dict
            Task ID → TaskResult
        """

        # ========================================================
        # VALIDATE TASKS
        # ========================================================

        if tasks is None:

            raise ValueError(
                "tasks cannot be None."
            )

        tasks = list(
            tasks
        )

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
        # PENDING TASKS
        # ========================================================

        pending = list(
            tasks
        )

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
            # NO READY TASKS
            # ====================================================

            if not ready_tasks:

                print(
                    "\n[Executor] "
                    "No executable tasks available."
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

                supervisor_decision = (

                    self.supervisor.decide(

                        pending
                    )
                )

                print(
                    "\n[Supervisor]"
                )

                print(
                    "Action:",
                    supervisor_decision.action
                )

                print(
                    "Reason:",
                    supervisor_decision.reason
                )

                raise RuntimeError(

                    "No executable tasks available. "
                    "Possible circular or unresolved "
                    "dependencies."
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
            # DYNAMIC CAPABILITY MATCHING
            # ====================================================

            agent_selection = (
                self._resolve_agent(
                    task
                )
            )

            if not agent_selection["success"]:

                error = (
                    agent_selection["error"]
                )

                print(
                    "\n[Capability Matcher] "
                    "Agent selection failed."
                )

                print(
                    "Reason:",
                    error
                )

                # ----------------------------------------------
                # Supervisor knows about the failure
                # ----------------------------------------------

                self.supervisor.task_failed(

                    task.id,

                    error
                )

                # ----------------------------------------------
                # Try recovery
                # ----------------------------------------------

                recovery = (

                    self._recover_task(

                        task,

                        error
                    )
                )

                # ----------------------------------------------
                # Process recovery decision
                # ----------------------------------------------

                action = (
                    recovery.action
                )

                if action == "RETRY":

                    print(
                        "\n↻ Retrying agent "
                        "selection."
                    )

                    self.retry_manager.wait(

                        self.retry_manager.decide(

                            task.id,

                            error
                        )
                    )

                    continue

                if action == "REPLAN":

                    print(
                        "\n↻ Replanning task."
                    )

                    results[
                        task.id
                    ] = self._failure_result(

                        task,

                        error
                    )

                    pending.remove(
                        task
                    )

                    continue

                if action == "ASK_USER":

                    print(
                        "\n⚠ User intervention "
                        "required."
                    )

                    results[
                        task.id
                    ] = self._failure_result(

                        task,

                        error
                    )

                    pending.remove(
                        task
                    )

                    continue

                # ----------------------------------------------
                # Permanent failure
                # ----------------------------------------------

                results[
                    task.id
                ] = self._failure_result(

                    task,

                    error
                )

                pending.remove(
                    task
                )

                continue

            # ====================================================
            # AGENT WAS SUCCESSFULLY RESOLVED
            # ====================================================

            selected_agent = (
                agent_selection["agent"]
            )

            if selected_agent:

                print(
                    "\n[Capability Matcher]"
                )

                print(
                    "Selected agent:",
                    selected_agent
                )

                # Set the selected agent on
                # the task so TaskRunner can use it.

                task.agent = (
                    selected_agent
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
                # Notify supervisor
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
                # Remove from pending
                # ----------------------------------------------

                pending.remove(
                    task
                )

                # ----------------------------------------------
                # Reset retries
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
            # SUPERVISOR: TASK FAILED
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
                    f"\n↻ Retrying task "
                    f"{task.id}..."
                )

                self.retry_manager.wait(

                    retry_decision
                )

                # Keep task in pending.

                continue

            # ====================================================
            # RETRIES EXHAUSTED
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

            # ====================================================
            # RECOVERY
            # ====================================================

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

                if recovery.replan_request:

                    print(
                        "Replan request:"
                    )

                    print(
                        recovery.replan_request
                    )

                results[
                    task.id
                ] = result

                pending.remove(
                    task
                )

                # Step 72 will replace this
                # task with dynamically generated
                # replacement tasks.

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

                # Step 71 capability matching
                # prepares the architecture for
                # automatic handoff.
                #
                # Step 72 will connect the selected
                # alternative agent back into the
                # task graph.

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
        Resolve the correct agent for a task.

        Priority:

        1. If task already specifies an agent,
           use it.

        2. If no agent is specified but required
           capabilities exist, use CapabilityMatcher.

        3. If neither exists, return an error.
        """

        # --------------------------------------------------------
        # Existing explicit agent
        # --------------------------------------------------------

        existing_agent = getattr(

            task,

            "agent",

            None
        )

        if existing_agent:

            return {

                "success": True,

                "agent":
                    existing_agent
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
                    "does not specify an agent "
                    "or required capabilities."
                )
            }

        # --------------------------------------------------------
        # Capability matcher unavailable
        # --------------------------------------------------------

        if self.capability_matcher is None:

            return {

                "success": False,

                "agent": None,

                "error": (
                    "CapabilityMatcher is not "
                    "configured."
                )
            }

        # --------------------------------------------------------
        # Find best agent
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
                    "Capability matching failed: "
                    f"{error}"
                )
            }

        # --------------------------------------------------------
        # No agent found
        # --------------------------------------------------------

        if agent is None:

            return {

                "success": False,

                "agent": None,

                "error": (

                    "No available agent has "
                    "the required capabilities: "

                    + ", ".join(
                        required_capabilities
                    )
                )
            }

        # --------------------------------------------------------
        # Return selected agent
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
                    "Capability matcher "
                    "returned an invalid "
                    "agent."
                )
            }

        return {

            "success": True,

            "agent":
                agent_name
        }

    # ============================================================
    # FAILURE RECOVERY
    # ============================================================

    def _recover_task(
        self,
        task,
        error
    ):
        """
        Send a failed task to RecoveryManager.

        Supports both the new RecoveryManager API
        and older implementations.
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

            # Backwards compatibility with
            # older RecoveryManager.

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
        Return True only when all dependencies
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

            # ----------------------------------------------------
            # Dependency hasn't executed.
            # ----------------------------------------------------

            if dependency_result is None:

                return False

            # ----------------------------------------------------
            # Dependency did not complete.
            # ----------------------------------------------------

            if (

                dependency_result.status

                != "completed"

            ):

                return False

        return True

    # ============================================================
    # CREATE FAILURE RESULT
    # ============================================================

    def _failure_result(
        self,
        task,
        error
    ):
        """
        Create a TaskResult for internal executor failures.
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