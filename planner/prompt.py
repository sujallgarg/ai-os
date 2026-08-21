from pydantic import BaseModel, Field


class PlannedTask(BaseModel):

    id: int

    description: str

    agent: str | None = None

    action: str

    tool_name: str | None = None

    parameters: dict = Field(
        default_factory=dict
    )

    depends_on: list[int] = Field(
        default_factory=list
    )

    priority: int = Field(
        default=5,
        ge=1,
        le=10
    )

    required_capabilities: list[str] = Field(
        default_factory=list
    )


class TaskPlan(BaseModel):

    goal: str

    tasks: list[PlannedTask]

    reasoning: str | None = None