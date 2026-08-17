from executor.result import (
    TaskResult
)

from timeout.manager import (
    TimeoutManager
)

from timeout.executor import (
    TimeoutExecutor
)


class TaskRunner:

    def __init__(
        self,
        agent_manager,
        log_service=None,
        timeout_manager=None
    ):

        self.agent_manager = (
            agent_manager
        )

        self.log_service = (
            log_service
        )

        self.timeout_manager = (

            timeout_manager

            or TimeoutManager()
        )

        self.timeout_executor = (
            TimeoutExecutor(
                self.timeout_manager
            )
        )

    def run(
        self,
        task,
        user_id="system"
    ):

        print(
            f"\n[TaskRunner] "
            f"Starting task {task.id}"
        )

        log = None

        # --------------------------------
        # Start execution log
        # --------------------------------

        if self.log_service:

            log = self.log_service.start(

                task_id=task.id,

                user_id=user_id,

                agent=task.agent,

                action=task.action
            )

        # --------------------------------
        # Actual agent function
        # --------------------------------

        def execute_agent():

            return (
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

        # --------------------------------
        # Execute with timeout
        # --------------------------------

        timeout_result, result = (

            self.timeout_executor.run(

                task,

                execute_agent
            )
        )

        # --------------------------------
        # SUCCESS
        # --------------------------------

        if (
            timeout_result.status
            == "completed"
        ):

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

        # --------------------------------
        # TIMEOUT
        # --------------------------------

        if (
            timeout_result.status
            == "timeout"
        ):

            error = (
                timeout_result.error
                or "Task timed out."
            )

            if self.log_service:

                self.log_service.fail(

                    log,

                    error=error
                )

            return TaskResult(

                task_id=task.id,

                status="failed",

                error=error
            )

        # --------------------------------
        # Unexpected result
        # --------------------------------

        return TaskResult(

            task_id=task.id,

            status="failed",

            error=(
                "Unknown execution state."
            )
        )