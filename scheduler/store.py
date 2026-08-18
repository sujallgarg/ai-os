class ScheduleStore:

    def __init__(self):

        self.tasks = {}

    def save(
        self,
        task
    ):

        self.tasks[
            task.id
        ] = task

    def get(
        self,
        task_id
    ):

        return self.tasks.get(
            task_id
        )

    def all(self):

        return list(
            self.tasks.values()
        )

    def delete(
        self,
        task_id
    ):

        self.tasks.pop(
            task_id,
            None
        )