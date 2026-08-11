from .base_agents import BaseAgent

class EmailAgent(BaseAgent):
    def execute(self,task):
        print(f"Processing email: {task}")
        return "Allemails read.."

    