from fastapi import (
    APIRouter,
    HTTPException
)

from api.dependencies import (
    application
)


router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"]
)


@router.get("")
def list_approvals():

    requests = (
        application
        .approval_manager
        .store
        .all()
    )

    return [

        {
            "id": request.id,

            "agent_id":
                request.agent_id,

            "tool_name":
                request.tool_name,

            "action":
                request.action,

            "parameters":
                request.parameters,

            "reason":
                request.reason,

            "status":
                request.status.value

        }

        for request in requests
    ]


@router.post(
    "/{request_id}/approve"
)
async def approve(
    request_id: str
):

    try:

        request = (
            application
            .approval_manager
            .approve(
                request_id
            )
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    # ------------------------------------------------------------
    # RESUME JOB
    # ------------------------------------------------------------

    job_id = (
        request.metadata.get(
            "job_id"
        )
        if hasattr(
            request,
            "metadata"
        )
        else None
    )

    if job_id:

        await application.resume_job(
            job_id
        )

    return {

        "id":
            request.id,

        "status":
            request.status.value,

        "resumed":
            bool(job_id)
    }


@router.post(
    "/{request_id}/reject"
)
def reject(
    request_id: str
):

    try:

        request = (
            application
            .approval_manager
            .reject(
                request_id
            )
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    return {

        "id":
            request.id,

        "status":
            request.status.value
    }