"""
Central retry manager.
"""

import time

from retry.models import (
    RetryConfig,
    RetryDecision
)

from retry.policy import (
    RetryPolicy
)

from retry.backoff import (
    ExponentialBackoff
)


class RetryManager:

    def __init__(
        self,
        config=None,
        policy=None
    ):

        self.config = (
            config
            or RetryConfig()
        )

        self.policy = (
            policy
            or RetryPolicy()
        )

        self.backoff = (
            ExponentialBackoff(

                initial_delay=(
                    self.config.initial_delay
                ),

                max_delay=(
                    self.config.max_delay
                ),

                multiplier=(
                    self.config.multiplier
                ),

                jitter=(
                    self.config.jitter
                )
            )
        )

        self.attempts = {}

    def decide(
        self,
        task_id: int,
        error: str
    ):

        error_type = (
            self.policy.classify(
                error
            )
        )

        attempt = (
            self.attempts.get(
                task_id,
                0
            )
        )

        # ----------------------------
        # Error cannot be retried
        # ----------------------------

        if not self.policy.is_retryable(
            error_type
        ):

            return RetryDecision(

                should_retry=False,

                attempt=attempt,

                delay=0,

                reason=(
                    "Error is not "
                    "retryable."
                ),

                error_type=error_type
            )

        # ----------------------------
        # Maximum attempts reached
        # ----------------------------

        if attempt >= (
            self.config.max_attempts
        ):

            return RetryDecision(

                should_retry=False,

                attempt=attempt,

                delay=0,

                reason=(
                    "Maximum retry "
                    "attempts reached."
                ),

                error_type=error_type
            )

        # ----------------------------
        # Record next attempt
        # ----------------------------

        next_attempt = (
            attempt + 1
        )

        self.attempts[
            task_id
        ] = next_attempt

        # ----------------------------
        # Calculate backoff
        # ----------------------------

        delay = (
            self.backoff.calculate(
                next_attempt
            )
        )

        return RetryDecision(

            should_retry=True,

            attempt=next_attempt,

            delay=delay,

            reason=(
                f"Retryable {error_type} "
                f"error."
            ),

            error_type=error_type
        )

    def wait(
        self,
        decision
    ):

        if decision.delay <= 0:

            return

        print(
            f"[Retry] Waiting "
            f"{decision.delay:.2f}s "
            f"before retry."
        )

        time.sleep(
            decision.delay
        )

    def reset(
        self,
        task_id: int
    ):

        self.attempts.pop(
            task_id,
            None
        )