from fastapi import APIRouter, HTTPException

from api.dependencies import (
    application
)


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.get("")
def list_jobs():

    jobs = (
        application.job_manager
        .store
        .all()
    )

    return [

        {
            "id": job.id,

            "goal": job.goal,

            "status": job.status.value,

            "progress": job.progress,

            "result": job.result,

            "error": job.error
        }

        for job in jobs
    ]


@router.get(
    "/{job_id}"
)
def get_job(
    job_id: str
):

    job = application.job_manager.get(
        job_id
    )

    if not job:

        raise HTTPException(

            status_code=404,

            detail="Job not found."
        )

    return {

        "id": job.id,

        "goal": job.goal,

        "status": job.status.value,

        "progress": job.progress,

        "result": job.result,

        "error": job.error
    }
