from monitoring.models import (
    GoalStatus
)


class GoalMonitor:

    def evaluate(
        self,
        goal,
        tasks,
        results
    ):

        total = len(tasks)

        completed = 0

        failed = 0

        for result in results.values():

            if result.status == "completed":

                completed += 1

            elif result.status == "failed":

                failed += 1

        pending = (
            total
            - completed
            - failed
        )

        if total == 0:

            progress = 100.0

        else:

            progress = (
                completed / total
            ) * 100

        if pending > 0:

            status = "in_progress"

        elif failed > 0:

            status = "partial_failure"

        else:

            status = "completed"

        return GoalStatus(

            goal=goal,

            total_tasks=total,

            completed_tasks=completed,

            failed_tasks=failed,

            pending_tasks=pending,

            progress=round(
                progress,
                2
            ),

            status=status
        )