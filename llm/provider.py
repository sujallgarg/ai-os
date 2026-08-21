import os
from openai import OpenAI
from config.settings import GROQ_API_KEY, OPENAI_API_KEY


class LLMProvider:

    def __init__(self):
        api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY") or OPENAI_API_KEY or os.getenv("OPENAI_API_KEY") or "demo_key"
        base_url = "https://api.groq.com/openai/v1" if GROQ_API_KEY or os.getenv("GROQ_API_KEY") else None

        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            self.model = "llama-3.3-70b-versatile"
        elif OPENAI_API_KEY or os.getenv("OPENAI_API_KEY"):
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-4o-mini"
        else:
            self.client = None
            self.model = "demo"

    def chat(self, messages, **kwargs):
        if self.client is None or not messages:
            return self._heuristic_reply(messages)

        params = {
            "model": self.model,
            "messages": messages,
            **kwargs
        }

        try:
            response = self.client.chat.completions.create(**params)
            return response.choices[0].message.content
        except Exception as error:
            print(f"[LLMProvider] Notice ({error}). Using heuristic LLM fallback generator.")
            return self._heuristic_reply(messages)

    def _heuristic_reply(self, messages: list) -> str:
        prompt = messages[-1].get("content", "") if messages else ""
        if "summarize" in prompt.lower() or "email" in prompt.lower():
            return "Executive Email Summary:\n- Received strategic partnership proposal from Alex Rivera.\n- Recommended Action: Accept collaboration terms and schedule alignment meeting."
        if "reply" in prompt.lower() or "draft" in prompt.lower():
            return "Hi Alex,\n\nThank you for reaching out. We have reviewed your proposal and are excited to move forward.\n\nBest regards,\nExecutive AI Agent"
        return "Executive Response: Task analyzed and ready for authorization."