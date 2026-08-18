from dataclasses import dataclass


@dataclass
class GoalStatus:

    goal: str

    total_tasks: int

    completed_tasks: int

    failed_tasks: int

    pending_tasks: int

    progress: float

    status: str