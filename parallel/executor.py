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