"""
Worker for executing one task.
"""

from parallel.models import (
    ParallelResult,
    ParallelTask
)


class AgentWorker:

    def __init__(
        self,
        agent_manager
    ):

        self.agent_manager = (
            agent_manager
        )

    def run(
        self,
        task: ParallelTask
    ):

        try:

            print(
                f"[Parallel] "
                f"{task.agent} started "
                f"task {task.task_id}"
            )

            result = (
                self.agent_manager.execute(

                    agent_name=task.agent,

                    task={

                        "id": task.task_id,

                        "action": task.action,

                        "description":
                            task.description,

                        "parameters":
                            task.parameters
                    }
                )
            )

            print(
                f"[Parallel] "
                f"{task.agent} completed "
                f"task {task.task_id}"
            )

            return ParallelResult(

                task_id=task.task_id,

                agent=task.agent,

                status="completed",

                output=result
            )

        except Exception as error:

            print(
                f"[Parallel] "
                f"{task.agent} failed: "
                f"{error}"
            )

            return ParallelResult(

                task_id=task.task_id,

                agent=task.agent,

                status="failed",

                error=str(error)
            )