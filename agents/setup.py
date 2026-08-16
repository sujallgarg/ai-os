from agents.agent_manager import AgentManager

from agents.email_agent import EmailAgent


def create_agent_manager():

    manager = AgentManager()

    email_agent = EmailAgent()

    manager.register(
        name="email",
        agent=email_agent
    )

    return manager