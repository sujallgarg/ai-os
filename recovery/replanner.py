"""
Recovery replanner.

Creates a request for the Planner when a task
cannot safely be completed using the current
execution strategy.
"""


class RecoveryReplanner:

    def __init__(
        self,
        planner=None
    ):

        self.planner = planner

    def should_replan(
        self,
        error: str,
        task
    ):

        if not error:

            return False

        error_lower = (
            error.lower()
        )

        # These errors often mean that
        # the current execution approach
        # is not appropriate.

        replanning_errors = [

            "invalid approach",

            "missing dependency",

            "unsupported",

            "tool unavailable",

            "agent unavailable",

            "cannot complete",

            "not possible"
        ]

        for pattern in (
            replanning_errors
        ):

            if pattern in error_lower:

                return True

        return False

    def create_replan_request(
        self,
        task,
        error: str
    ):

        return {

            "task_id":
                task.id,

            "original_goal":
                task.description,

            "agent":
                task.agent,

            "action":
                task.action,

            "parameters":
                task.parameters,

            "error":
                error,

            "request":
                (
                    "Create an alternative "
                    "execution strategy."
                )
        }