"""
Autonomous AI background worker.
"""

import asyncio

from api.dependencies import (
    application
)

from workers.queue import (
    job_queue
)

from workers.job_runner import (
    JobRunner
)


class BackgroundWorker:

    def __init__(self):

        self.runner = JobRunner(
            application
        )

        self.running = True

    async def start(self):

        print(
            "=" * 60
        )

        print(
            "AI BACKGROUND WORKER"
        )

        print(
            "=" * 60
        )

        print(
            "Worker is ready."
        )

        while self.running:

            try:

                job_id = (
                    await job_queue.dequeue()
                )

                print(
                    "\n[Worker] Received job:",
                    job_id
                )

                try:

                    await self.runner.run(
                        job_id
                    )

                finally:

                    job_queue.task_done()

            except asyncio.CancelledError:

                print(
                    "[Worker] Shutdown requested."
                )

                break

            except Exception as error:

                print(
                    "[Worker] Unexpected error:"
                )

                print(
                    str(error)
                )

    def stop(self):

        self.running = False


async def main():

    worker = BackgroundWorker()

    await worker.start()


if __name__ == "__main__":

    asyncio.run(
        main()
    )