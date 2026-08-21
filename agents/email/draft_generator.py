"""
AI Email Draft Generator.
Generates email replies based on the user's instruction and the existing email conversation.
This module ONLY creates drafts. It does not send emails directly.
"""

from llm.provider import LLMProvider


class EmailDraftGenerator:

    def __init__(self):
        self.llm = LLMProvider()

    def generate_reply(
        self,
        thread,
        instruction
    ):
        if not thread:
            thread = {
                "thread_id": "demo_thread_001",
                "messages": [
                    {
                        "from": "Alex Rivera <alex.rivera@partnerorg.com>",
                        "to": "me",
                        "date": "Fri, 21 Aug 2026 14:00:00 GMT",
                        "subject": "[Demo] Strategic Partnership & Integration Proposal",
                        "body": "Hi Team,\n\nWe reviewed your AI platform and would love to explore a joint executive integration. Attached is our proposal outline.\n\nBest,\nAlex"
                    }
                ]
            }

        if not instruction:
            instruction = "Generate polite executive acceptance reply."

        conversation = self._format_thread(thread)

        prompt = f"""
You are an AI email assistant.
Your job is to create a professional email reply.
Read the conversation below and follow the user's instruction.

USER INSTRUCTION:
{instruction}

EMAIL CONVERSATION:
{conversation}

Rules:
1. Do not invent facts.
2. Do not claim something was completed if it wasn't.
3. Keep the reply concise.
4. Match the tone of the conversation.
5. Return only the email body.
"""

        messages = [
            {
                "role": "system",
                "content": "You are a careful and professional email drafting assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        return self.llm.chat(messages)

    def _format_thread(self, thread):
        if isinstance(thread, dict):
            messages = thread.get("messages", [])
        elif isinstance(thread, list):
            messages = thread
        else:
            messages = []

        formatted = []
        for message in messages:
            if isinstance(message, dict):
                formatted.append(
                    f"FROM: {message.get('from', '')}\nTO: {message.get('to', '')}\nDATE: {message.get('date', '')}\nSUBJECT: {message.get('subject', '')}\n\nBODY:\n{message.get('body', '')}\n------------------------------"
                )

        return "\n".join(formatted)