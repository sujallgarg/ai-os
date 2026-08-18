from fastapi import APIRouter, HTTPException

from api.models import (
    GoalRequest,
    GoalResponse
)

from api.dependencies import (
    application
)


router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)


@router.post(
    "",
    response_model=GoalResponse
)
def create_goal(
    request: GoalRequest
):

    # ============================================================
    # CREATE JOB
    # ============================================================

    job = application.job_manager.create(
        request.goal
    )

    return GoalResponse(

        job_id=job.id,

        goal=job.goal,

        status=job.status.value
    )


@router.get(
    "/{job_id}"
)
def get_goal(
    job_id: str
):

    job = application.job_manager.get(
        job_id
    )

    if not job:

        raise HTTPException(

            status_code=404,

            detail="Goal not found."
        )

    return {

        "job_id": job.id,

        "goal": job.goal,

        "status": job.status.value,

        "progress": job.progress,

        "result": job.result,

        "error": job.error
    }