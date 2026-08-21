from agents.agent_manager import AgentManager
from agents.email_agent import EmailAgent
from agents.general_agent import GeneralAgent


def create_agent_manager():

    manager = AgentManager()

    email_agent = EmailAgent()
    general_agent = GeneralAgent()

    manager.register(
        name="email",
        agent=email_agent
    )

    for name in ["coding", "browser", "calendar", "file", "supervisor", "general"]:

        manager.register(
            name=name,
            agent=general_agent
        )

    return manager