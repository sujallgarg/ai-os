from dataclasses import dataclass, field


@dataclass
class PlanStep:

    id: int

    description: str

    agent: str

    action: str

    parameters: dict = field(
        default_factory=dict
    )

    depends_on: list[int] = field(
        default_factory=list
    )


@dataclass
class TaskPlan:

    goal: str

    steps: list[PlanStep] = field(
        default_factory=list
    )


@dataclass
class ExecutionTask:

    id: int

    description: str

    agent: str

    action: str

    parameters: dict = field(
        default_factory=dict
    )

    depends_on: list[int] = field(
        default_factory=list
    )

    status: str = "pending"