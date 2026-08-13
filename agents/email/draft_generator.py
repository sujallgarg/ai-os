"""
AI Email Draft Generator.

Generates email replies based on the user's instruction
and the existing email conversation.

This module ONLY creates drafts.
It does not send emails.
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
            raise ValueError(
                "Email thread is required."
            )

        if not instruction:
            raise ValueError(
                "Reply instruction is required."
            )

        conversation = self._format_thread(
            thread
        )

        prompt = f"""
You are an AI email assistant.

Your job is to create a professional email reply.

Read the conversation below and follow the
user's instruction.

USER INSTRUCTION:
{instruction}

EMAIL CONVERSATION:
{conversation}

Rules:

1. Do not invent facts.
2. Do not claim something was completed if it wasn't.
3. Keep the reply concise.
4. Match the tone of the conversation.
5. Do not include a subject unless necessary.
6. Return only the email body.
"""

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a careful and professional "
                    "email drafting assistant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        return self.llm.chat(
            messages
        )

    def _format_thread(self, thread):

        messages = thread.get(
            "messages",
            []
        )

        formatted = []

        for message in messages:

            formatted.append(
                f"""
FROM: {message.get("from", "")}
TO: {message.get("to", "")}
DATE: {message.get("date", "")}
SUBJECT: {message.get("subject", "")}

BODY:
{message.get("body", "")}

------------------------------
"""
            )

        return "\n".join(formatted)