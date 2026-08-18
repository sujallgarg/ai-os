from dataclasses import dataclass, field


@dataclass
class ExecutionTask:

    id: int

    description: str

    agent: str | None

    action: str

    parameters: dict = field(
        default_factory=dict
    )

    depends_on: list[int] = field(
        default_factory=list
    )

    priority: int = 5

    required_capabilities: list[str] = field(
        default_factory=list
    )

    status: str = "pending"