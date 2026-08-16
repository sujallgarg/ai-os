"""
Retry management.
"""


class RetryManager:

    def __init__(
        self,
        max_retries=3
    ):

        self.max_retries = (
            max_retries
        )

        self.attempts = {}

    def can_retry(
        self,
        task_id: int
    ):

        attempts = self.attempts.get(
            task_id,
            0
        )

        return (
            attempts < self.max_retries
        )

    def record_attempt(
        self,
        task_id: int
    ):

        self.attempts[task_id] = (
            self.attempts.get(
                task_id,
                0
            ) + 1
        )

    def get_attempts(
        self,
        task_id: int
    ):

        return self.attempts.get(
            task_id,
            0
        )

    def reset(
        self,
        task_id: int
    ):

        self.attempts.pop(
            task_id,
            None
        )