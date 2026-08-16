from executor.result import TaskResult


class TaskRunner:

    def __init__(
        self,
        agent_manager,
        log_service=None
    ):

        self.agent_manager = (
            agent_manager
        )

        self.log_service = (
            log_service
        )

    def run(
        self,
        task,
        user_id="system"
    ):

        print(
            f"[Executor] Starting task "
            f"{task.id}: "
            f"{task.description}"
        )

        log = None

        if self.log_service:

            log = self.log_service.start(

                task_id=task.id,

                user_id=user_id,

                agent=task.agent,

                action=task.action
            )

        try:

            result = (
                self.agent_manager.execute(

                    agent_name=task.agent,

                    task={
                        "id": task.id,

                        "action":
                            task.action,

                        "parameters":
                            task.parameters,

                        "description":
                            task.description
                    }
                )
            )

            if self.log_service:

                self.log_service.complete(

                    log,

                    output=result
                )

            return TaskResult(

                task_id=task.id,

                status="completed",

                output=result
            )

        except Exception as error:

            if self.log_service:

                self.log_service.fail(

                    log,

                    error=str(error)
                )

            return TaskResult(

                task_id=task.id,

                status="failed",

                error=str(error)
            )