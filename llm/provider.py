from openai import OpenAI
from config.settings import GROQ_API_KEY


class LLMProvider:
    def __init__(self):
        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

    def chat(self, messages, **kwargs):
        params = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            **kwargs
        }
        response = self.client.chat.completions.create(**params)
        return response.choices[0].message.content



        