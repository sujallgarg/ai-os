from fastapi import APIRouter, HTTPException, Body
from api.dependencies import application
from agents.email_agent import EmailAgent

router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)

email_agent_instance = EmailAgent()


@router.get("")
def list_agents():
    agents = application.agent_registry.all()
    return [
        {
            "name": agent.name,
            "description": agent.description,
            "capabilities": agent.capabilities,
            "tools": agent.tools,
            "priority": agent.priority,
            "status": agent.status
        }
        for agent in agents
    ]


@router.post("/email/execute")
def execute_email_agent(payload: dict = Body(...)):
    """
    Execute Email Agent actions directly:
    read, search, thread, summarize, draft_reply, create_draft, send_email, reply, forward, classify
    """
    try:
        result = email_agent_instance.execute(payload)
        return {"status": "success", "action": payload.get("action", "read"), "result": result}
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))