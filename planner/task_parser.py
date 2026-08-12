from llm.provider import LLMProvider
from planner.planner_prompt import SYSTEM_PROMPT


class TaskParser:
    def __init__(self):
        self.llm = LLMProvider()

    def parse(self,text):
        messages=[
            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content":text
                
            }
        ]

        return self.llm.chat(messages)
        