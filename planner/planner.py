from planner.task_parser import TaskParser
from planner.task_router import TaskRouter
from planner.json_parser import JsonParser
from planner.reflection import Reflection


class Planner:
    def __init__(self, memory, agent_manager):
        self.parser = TaskParser()
        self.router = TaskRouter()
        self.agent = agent_manager
        self.memory = memory
        self.json = JsonParser()
        self.reflection = Reflection()

    def run(self, text):
        context = self.memory.recall(text)

        if isinstance(context, list):
            context_str = "\n".join(str(c) for c in context if c)
        else:
            context_str = str(context) if context else ""

        full_prompt = f"{context_str}\n{text}".strip() if context_str else text

        task_response = self.parser.parse(full_prompt)
        self.memory.remember(text)
        task = self.json.parse(task_response)
        agent = self.router.route(task)

        result = self.agent.execute(agent, task)

        verified = self.reflection.verify(result)
        if verified:
            self.memory.remember(text)

        return result

