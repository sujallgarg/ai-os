import uuid

from datetime import datetime

from scheduler.models import (
    ScheduledTask
)

from scheduler.store import (
    ScheduleStore
)


class TaskScheduler:

    def __init__(
        self,
        executor,
        store=None
    ):

        self.executor = executor

        self.store = (
            store
            or ScheduleStore()
        )

    def schedule(
        self,
        task_data,
        run_at,
        recurring=False,
        interval_seconds=None
    ):

        task = ScheduledTask(

            id=str(
                uuid.uuid4()
            ),

            task_data=task_data,

            run_at=run_at,

            recurring=recurring,

            interval_seconds=(
                interval_seconds
            )
        )

        self.store.save(
            task
        )

        return task

    def run_due_tasks(self):

        now = datetime.utcnow()

        due_tasks = [

            task

            for task
            in self.store.all()

            if (
                task.enabled
                and task.run_at <= now
            )
        ]

        for task in due_tasks:

            self.executor.execute(

                task.task_data
            )

            if task.recurring:

                from datetime import timedelta

                task.run_at = (

                    now

                    + timedelta(
                        seconds=(
                            task.interval_seconds
                            or 86400
                        )
                    )
                )

            else:

                task.enabled = False

        return due_tasks