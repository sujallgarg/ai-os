from planner.task_parser import TaskParser
from planner.task_router import TaskRouter

class Planner:
    def __init__(self,memory,agent_manager):
        self.parser = TaskParser()
        self.router = TaskRouter()
        self.agent = agent_manager
        self.memory=memory

    def run(self, text):

        context = self.memory.recall(text)
        task = self.parser.parse(
            context+"\n"+text
        )
        self.memory.remember(text)
        task = self.json.parse(task)
        agent = self.router.route(task)

        result =self.agent.execute(agent,task)
        return result

        verfied = self.reflection.verify(result)
        if verfied:
            self.memory,remember(text)
        return result
