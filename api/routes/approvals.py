from fastapi import APIRouter, HTTPException

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
        application.approval_manager
        .store
        .all()
    )

    return [

        {
            "id": request.id,

            "agent_id": request.agent_id,

            "tool_name": request.tool_name,

            "action": request.action,

            "parameters": request.parameters,

            "reason": request.reason,

            "status": request.status.value
        }

        for request in requests
    ]


@router.post(
    "/{request_id}/approve"
)
def approve(
    request_id: str
):

    try:

        request = (
            application.approval_manager
            .approve(request_id)
        )

    except ValueError as error:

        raise HTTPException(

            status_code=404,

            detail=str(error)
        )

    return {

        "id": request.id,

        "status": request.status.value
    }


@router.post(
    "/{request_id}/reject"
)
def reject(
    request_id: str
):

    try:

        request = (
            application.approval_manager
            .reject(request_id)
        )

    except ValueError as error:

        raise HTTPException(

            status_code=404,

            detail=str(error)
        )

    return {

        "id": request.id,

        "status": request.status.value
    }