"""
Calculates task priority.
"""


class PriorityCalculator:

    LEVELS = {
        "critical": 10,
        "high": 8,
        "normal": 5,
        "low": 3,
        "background": 1
    }

    def calculate(
        self,
        level="normal",
        urgency=0,
        importance=0,
        deadline_pressure=0
    ):

        base = self.LEVELS.get(
            level,
            self.LEVELS["normal"]
        )

        score = (
            base
            + urgency
            + importance
            + deadline_pressure
        )

        # Keep priority within 1–100
        score = max(
            1,
            min(score, 100)
        )

        return score