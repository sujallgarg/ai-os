"""
Execution state manager.
"""


class ExecutionStateManager:

    def __init__(
        self,
        goal,
        total_tasks
    ):

        self.goal = goal

        self.total_tasks = (
            total_tasks
        )

        self.completed_tasks = 0

        self.failed_tasks = 0

        self.running_tasks = 0

        self.pending_tasks = (
            total_tasks
        )

        self.status = "running"

        self.results = {}

    def task_started(
        self,
        task_id
    ):

        self.running_tasks += 1

        self.pending_tasks = max(

            0,

            self.pending_tasks - 1
        )

        self.results[
            task_id
        ] = {
            "status": "running"
        }

    def task_completed(
        self,
        task_id,
        result=None
    ):

        self.running_tasks = max(

            0,

            self.running_tasks - 1
        )

        self.completed_tasks += 1

        self.results[
            task_id
        ] = {

            "status": "completed",

            "result": result
        }

        self._update_status()

    def task_failed(
        self,
        task_id,
        error=None
    ):

        self.running_tasks = max(

            0,

            self.running_tasks - 1
        )

        self.failed_tasks += 1

        self.results[
            task_id
        ] = {

            "status": "failed",

            "error": error
        }

        self._update_status()

    def _update_status(self):

        if (
            self.completed_tasks
            >= self.total_tasks
        ):

            self.status = "completed"

            return

        if self.failed_tasks > 0:

            self.status = "attention"

            return

        self.status = "running"

    def snapshot(self):

        return {

            "goal":
                self.goal,

            "total_tasks":
                self.total_tasks,

            "completed_tasks":
                self.completed_tasks,

            "failed_tasks":
                self.failed_tasks,

            "running_tasks":
                self.running_tasks,

            "pending_tasks":
                self.pending_tasks,

            "status":
                self.status
        }