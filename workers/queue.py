"""
Background job queue.

Development implementation uses asyncio.Queue.

Production can replace this with Redis/RQ/Celery
without changing the API layer.
"""

import asyncio


class JobQueue:

    def __init__(self):

        self.queue = asyncio.Queue()

    async def enqueue(
        self,
        job_id: str
    ):

        await self.queue.put(
            job_id
        )

    async def dequeue(
        self
    ):

        return await self.queue.get()

    def task_done(self):

        self.queue.task_done()

    def size(self):

        return self.queue.qsize()


job_queue = JobQueue()