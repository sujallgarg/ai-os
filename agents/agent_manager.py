from agents.email_agent import EmailAgent
from agents.general_agent import GeneralAgent
class AgentManager:
    def __init__(self):
        self.email = EmailAgent()
        self.general=GeneralAgent()
    def execute(self,agent,task):
        if agent=="email":
            return self.email.execute(task)
        elif agent=="general":
            return self.general.execute(task)


        
