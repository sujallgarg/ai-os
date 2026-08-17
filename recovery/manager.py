"""
Central failure recovery manager.
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

from recovery.replanner import (
    RecoveryReplanner
)


class RecoveryManager:

    def __init__(
        self,
        max_retries=3,
        planner=None
    ):

        self.retry_manager = (
            RetryManager(
                max_retries
            )
        )

        self.analyzer = (
            ErrorAnalyzer()
        )

        self.replanner = (
            RecoveryReplanner(
                planner
            )
        )

    def handle_failure(
        self,
        task_id: int,
        error: str,
        task=None
    ):

        error_type = (
            self.analyzer.analyze(
                error
            )
        )

        attempts = (
            self.retry_manager
            .get_attempts(
                task_id
            )
        )

        # --------------------------------
        # Temporary error
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
                        "Temporary failure. "
                        "Retry is safe."
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
                    "The task requires "
                    "user intervention."
                ),

                retry_count=attempts
            )

        # --------------------------------
        # Try replanning
        # --------------------------------

        if task is not None:

            if self.replanner.should_replan(
                error,
                task
            ):

                request = (
                    self.replanner
                    .create_replan_request(
                        task,
                        error
                    )
                )

                return RecoveryDecision(

                    action="REPLAN",

                    reason=(
                        "The current execution "
                        "strategy is not suitable."
                    ),

                    retry_count=attempts,

                    replan_request=request
                )

        # --------------------------------
        # Permanent failure
        # --------------------------------

        return RecoveryDecision(

            action="FAIL",

            reason=(
                "The task cannot be "
                "safely recovered."
            ),

            retry_count=attempts
        )