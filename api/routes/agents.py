from fastapi import APIRouter

from api.dependencies import (
    application
)


router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)


@router.get("")
def list_agents():

    agents = (
        application.agent_registry
        .all()
    )

    return [

        {
            "name": agent.name,

            "description":
                agent.description,

            "capabilities":
                agent.capabilities,

            "tools":
                agent.tools,

            "priority":
                agent.priority,

            "status":
                agent.status
        }

        for agent in agents
    ]