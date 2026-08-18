from fastapi import APIRouter

from api.dependencies import (
    application
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/memory")
def memory():

    memories = (
        application.memory_manager
        .store
        .all()
    )

    return [

        {
            "key": memory.key,

            "value": memory.value,

            "agent_id":
                memory.agent_id,

            "type":
                memory.memory_type,

            "importance":
                memory.importance
        }

        for memory in memories
    ]