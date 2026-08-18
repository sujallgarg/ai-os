class JobStore:

    def __init__(self):

        self.jobs = {}

    def save(
        self,
        job
    ):

        self.jobs[
            job.id
        ] = job

    def get(
        self,
        job_id
    ):

        return self.jobs.get(
            job_id
        )

    def all(self):

        return list(
            self.jobs.values()
        )