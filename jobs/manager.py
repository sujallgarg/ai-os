import uuid
from datetime import datetime

from jobs.models import (
    Job,
    JobStatus
)

from jobs.store import (
    JobStore
)


class JobManager:

    def __init__(
        self,
        store=None
    ):
        self.store = (
            store
            or JobStore()
        )

    def create(
        self,
        goal
    ):
        job = Job(
            id=str(
                uuid.uuid4()
            ),
            goal=goal
        )

        self.store.save(
            job
        )

        return job

    def start(
        self,
        job_id
    ):
        job = self.store.get(
            job_id
        )

        if not job:
            raise ValueError(
                "Job not found."
            )

        job.status = (
            JobStatus.RUNNING
        )

        return job

    def update_progress(
        self,
        job_id,
        progress
    ):
        job = self.store.get(
            job_id
        )

        if not job:
            raise ValueError(
                "Job not found."
            )

        job.progress = max(
            0,
            min(
                100,
                progress
            )
        )

        return job

    def wait_for_approval(
        self,
        job_id,
        task_id=None,
        approval_id=None
    ):
        job = self.store.get(
            job_id
        )

        if not job:
            raise ValueError(
                "Job not found."
            )

        job.status = (
            JobStatus.WAITING_FOR_APPROVAL
        )

        job.current_task_id = task_id
        job.pending_approval_id = approval_id
        job.updated_at = datetime.utcnow()

        return job

    def complete(
        self,
        job_id,
        result=None
    ):
        job = self.store.get(
            job_id
        )

        if not job:
            raise ValueError(
                "Job not found."
            )

        job.status = (
            JobStatus.COMPLETED
        )

        job.progress = 100
        job.result = result

        return job

    def fail(
        self,
        job_id,
        error
    ):
        job = self.store.get(
            job_id
        )

        if not job:
            raise ValueError(
                "Job not found."
            )

        job.status = (
            JobStatus.FAILED
        )

        job.error = error

        return job

    def get(
        self,
        job_id
    ):
        return self.store.get(
            job_id
        )