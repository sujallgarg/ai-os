"""
Exponential backoff calculation.
"""

import random


class ExponentialBackoff:

    def __init__(
        self,
        initial_delay=1.0,
        max_delay=30.0,
        multiplier=2.0,
        jitter=0.2
    ):

        self.initial_delay = (
            initial_delay
        )

        self.max_delay = (
            max_delay
        )

        self.multiplier = (
            multiplier
        )

        self.jitter = (
            jitter
        )

    def calculate(
        self,
        attempt: int
    ):

        delay = (
            self.initial_delay
            * (
                self.multiplier
                ** max(attempt - 1, 0)
            )
        )

        delay = min(
            delay,
            self.max_delay
        )

        # Small random variation prevents
        # many workers from retrying at
        # exactly the same time.
        variation = (
            random.uniform(
                -self.jitter,
                self.jitter
            )
        )

        delay = (
            delay
            * (1 + variation)
        )

        return max(
            0,
            delay
        )