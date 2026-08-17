"""
Task priority manager.
"""

from priority.calculator import (
    PriorityCalculator
)


class PriorityManager:

    def __init__(self):

        self.calculator = (
            PriorityCalculator()
        )

    def assign(
        self,
        task,
        level="normal",
        urgency=0,
        importance=0,
        deadline_pressure=0
    ):

        score = self.calculator.calculate(

            level=level,

            urgency=urgency,

            importance=importance,

            deadline_pressure=deadline_pressure
        )

        task.priority = score

        return task

    def sort(
        self,
        tasks
    ):

        return sorted(

            tasks,

            key=lambda task:
                getattr(
                    task,
                    "priority",
                    5
                ),

            reverse=True
        )