from pydantic import BaseModel, Field


class GoalRequest(BaseModel):

    goal: str = Field(
        min_length=1,
        max_length=10000
    )


class GoalResponse(BaseModel):

    job_id: str

    goal: str

    status: str


class ApprovalResponse(BaseModel):

    request_id: str

    status: str


class HealthResponse(BaseModel):

    status: str

    service: str