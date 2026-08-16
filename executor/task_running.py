"""
Runs individual execution tasks.
"""

from executor.result import TaskResult


class TaskRunner:

    def __init__(
        self,
        agent_manager
    ):

        self.agent_manager = (
            agent_manager
        )

    def run(
        self,
        task
    ):

        print(
            f"[Executor] Starting task "
            f"{task.id}: "
            f"{task.description}"
        )

        try:

            result = (
                self.agent_manager.execute(
                    agent_name=task.agent,
                    task={
                        "id": task.id,
                        "action": task.action,
                        "parameters": task.parameters,
                        "description": task.description
                    }
                )
            )

            return TaskResult(

                task_id=task.id,

                status="completed",

                output=result
            )

        except Exception as error:

            print(
                f"[Executor] Task {task.id} failed: "
                f"{error}"
            )

            return TaskResult(

                task_id=task.id,

                status="failed",

                error=str(error)
            )