"""
Parallel agent executor.
"""

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from parallel.worker import (
    AgentWorker
)


class ParallelExecutor:

    def __init__(
        self,
        agent_manager,
        max_workers=5
    ):

        self.worker = AgentWorker(
            agent_manager
        )

        self.max_workers = (
            max_workers
        )

    def execute(
        self,
        tasks
    ):

        results = []

        with ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:

            futures = {

                executor.submit(
                    self.worker.run,
                    task
                ): task

                for task in tasks
            }

            for future in as_completed(
                futures
            ):

                result = future.result()

                results.append(
                    result
                )

        return results
        # ====================================================
# RECOVERY → REPLAN
# ====================================================

        if recovery.action == "REPLAN":

            print(
                "\n↻ Dynamic replanning required."
            )

    # ------------------------------------------------
    # Ask Supervisor/Replanner for new tasks
    # ------------------------------------------------

        try:

            new_graph = (
                self.supervisor.replan_task(

                    task,

                error
            )
        )

        except Exception as replan_error:

            print(
                "\n[Replanner] Failed:"
            )

        print(
            replan_error
        )

        results[
            task.id
        ] = result

        pending.remove(
            task
        )

                            

    # ------------------------------------------------
    # Remove failed task
    # ------------------------------------------------

        results[
            task.id
        ] = result

        pending.remove(
            task
    )

    # ------------------------------------------------
    # Add replacement tasks
    # ------------------------------------------------

        replacement_tasks = list(
            new_graph.tasks.values()
        )

        print(
            "\n[Replanner] Generated "
        f"{len(replacement_tasks)} "
        "replacement tasks."
    )

    # ------------------------------------------------
    # Add replacement tasks to queue
    # ------------------------------------------------

        for replacement_task in (
            replacement_tasks
        ):

             print(
                 "\nNew task:"
             )

             print(
                 "  ID:",
            replacement_task.id
        )

        print(
                "  Description:",
                replacement_task.description
            )

        print(
                "  Action:",
                replacement_task.action
            )

        print(
                "  Capabilities:",
                replacement_task.required_capabilities
            )

        pending.append(
                replacement_task
            )

        