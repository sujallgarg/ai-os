from dataclasses import dataclass, field


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

    priority: int = 5


@dataclass
class PlanResult:

    goal: str

    tasks: list[ExecutionTask]

    metadata: dict = field(
        default_factory=dict
    )