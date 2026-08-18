"""
Supervisor monitoring logic.
"""


class SupervisorMonitor:

    def inspect(
        self,
        state,
        pending_tasks
    ):

        # --------------------------------
        # Everything completed
        # --------------------------------

        if state.completed_tasks >= (
            state.total_tasks
        ):

            return {

                "status":
                    "completed",

                "reason":
                    "All tasks completed."
            }

        # --------------------------------
        # Failed task
        # --------------------------------

        if state.failed_tasks > 0:

            return {

                "status":
                    "attention",

                "reason":
                    "One or more tasks failed."
            }

        # --------------------------------
        # No pending tasks but not complete
        # --------------------------------

        if (
            not pending_tasks
            and state.completed_tasks
            < state.total_tasks
        ):

            return {

                "status":
                    "blocked",

                "reason":
                    "Execution is blocked."
            }

        # --------------------------------
        # Normal execution
        # --------------------------------

        return {

            "status":
                "running",

            "reason":
                "Execution is progressing."
        }