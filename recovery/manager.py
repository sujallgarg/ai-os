"""
Central error recovery manager.
"""

from recovery.retry import (
    RetryManager
)

from recovery.analyzer import (
    ErrorAnalyzer
)

from recovery.models import (
    RecoveryDecision
)


class RecoveryManager:

    def __init__(
        self,
        max_retries=3
    ):

        self.retry_manager = (
            RetryManager(
                max_retries
            )
        )

        self.analyzer = (
            ErrorAnalyzer()
        )

    def handle_failure(
        self,
        task_id: int,
        error: str
    ):

        error_type = (
            self.analyzer.analyze(
                error
            )
        )

        attempts = (
            self.retry_manager
            .get_attempts(task_id)
        )

        # --------------------------------
        # Retryable error
        # --------------------------------

        if error_type == "RETRYABLE":

            if self.retry_manager.can_retry(
                task_id
            ):

                self.retry_manager.record_attempt(
                    task_id
                )

                return RecoveryDecision(

                    action="RETRY",

                    reason=(
                        "Temporary error. "
                        "Retrying task."
                    ),

                    retry_count=(
                        attempts + 1
                    )
                )

        # --------------------------------
        # User intervention
        # --------------------------------

        if error_type == "USER_REQUIRED":

            return RecoveryDecision(

                action="ASK_USER",

                reason=(
                    "This task requires "
                    "user intervention."
                ),

                retry_count=attempts
            )

        # --------------------------------
        # Unknown/non-retryable
        # --------------------------------

        return RecoveryDecision(

            action="FAIL",

            reason=(
                "Task cannot safely "
                "be retried."
            ),

            retry_count=attempts
        )