"""
Supervisor Agent.

Coordinates the overall execution of
a multi-agent plan.
"""

from supervisor.state import (
    ExecutionStateManager
)

from supervisor.monitor import (
    SupervisorMonitor
)

from supervisor.models import (
    SupervisorDecision
)


class SupervisorAgent:

    def __init__(
        self,
        planner=None,
        recovery_manager=None
    ):

        self.planner = planner

        self.recovery = (
            recovery_manager
        )

        self.monitor = (
            SupervisorMonitor()
        )

        self.state = None

    # ============================================================
    # START PLAN
    # ============================================================

    def start(
        self,
        goal,
        tasks
    ):

        self.state = (
            ExecutionStateManager(

                goal=goal,

                total_tasks=len(tasks)
            )
        )

        return self.state.snapshot()

    # ============================================================
    # TASK STARTED
    # ============================================================

    def task_started(
        self,
        task_id
    ):

        if not self.state:

            raise RuntimeError(
                "Supervisor has not started."
            )

        self.state.task_started(
            task_id
        )

    # ============================================================
    # TASK COMPLETED
    # ============================================================

    def task_completed(
        self,
        task_id,
        result=None
    ):

        if not self.state:

            raise RuntimeError(
                "Supervisor has not started."
            )

        self.state.task_completed(

            task_id,

            result
        )

    # ============================================================
    # TASK FAILED
    # ============================================================

    def task_failed(
        self,
        task_id,
        error=None
    ):

        if not self.state:

            raise RuntimeError(
                "Supervisor has not started."
            )

        self.state.task_failed(

            task_id,

            error
        )

    # ============================================================
    # DECIDE WHAT TO DO
    # ============================================================

    def decide(
        self,
        pending_tasks
    ):

        if not self.state:

            raise RuntimeError(
                "Supervisor has not started."
            )

        inspection = (
            self.monitor.inspect(

                self.state,

                pending_tasks
            )
        )

        status = inspection[
            "status"
        ]

        reason = inspection[
            "reason"
        ]

        # --------------------------------
        # COMPLETE
        # --------------------------------

        if status == "completed":

            return SupervisorDecision(

                action="COMPLETE",

                reason=reason
            )

        # --------------------------------
        # ATTENTION
        # --------------------------------

        if status == "attention":

            return SupervisorDecision(

                action="RECOVER",

                reason=reason
            )

        # --------------------------------
        # BLOCKED
        # --------------------------------

        if status == "blocked":

            return SupervisorDecision(

                action="REPLAN",

                reason=reason
            )

        # --------------------------------
        # CONTINUE
        # --------------------------------

        return SupervisorDecision(

            action="CONTINUE",

            reason=reason
        )

    # ============================================================
    # GET STATE
    # ============================================================

    def get_state(self):

        if not self.state:

            return None

        return self.state.snapshot()