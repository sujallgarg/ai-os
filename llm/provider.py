from openai import OpenAI
from config.settings import OPENAI_API_KEY

class LLMProvider:
    def __init_(self):
        self.client=OpenAI(api_key=OPENAI_API_KEY)
    def chat(self,messages):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response.choices[0].message.content


        