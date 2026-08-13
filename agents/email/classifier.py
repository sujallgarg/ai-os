"""
AI Email Classifier.

Classifies emails based on their content and determines
whether they require user attention or a reply.
"""

import json

from llm.provider import LLMProvider


class EmailClassifier:

    def __init__(self):

        self.llm = LLMProvider()

    def classify(
        self,
        email: dict
    ):

        if not email:

            raise ValueError(
                "Email data is required."
            )

        prompt = f"""
You are an AI email classification assistant.

Analyze the following email.

FROM:
{email.get("from", "")}

TO:
{email.get("to", "")}

SUBJECT:
{email.get("subject", "")}

BODY:
{email.get("body", "")}

Classify the email using these fields:

category:
Choose ONE:
- work
- client
- personal
- finance
- newsletter
- marketing
- notification
- spam
- other

priority:
Choose ONE:
- low
- medium
- high
- urgent

requires_reply:
Choose true or false.

requires_action:
Choose true or false.

sentiment:
Choose ONE:
- positive
- neutral
- negative

reason:
Give a short explanation.

Return ONLY valid JSON.

Example:

{{
    "category": "client",
    "priority": "high",
    "requires_reply": true,
    "requires_action": true,
    "sentiment": "neutral",
    "reason": "The client is requesting an update."
}}
"""

        messages = [
            {
                "role": "system",
                "content": (
                    "You classify emails accurately "
                    "and return valid JSON only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = self.llm.chat(
            messages
        )

        return self._parse_response(
            response
        )

    def _parse_response(
        self,
        response
    ):

        if isinstance(response, dict):

            return response

        try:

            return json.loads(
                response
            )

        except json.JSONDecodeError:

            raise ValueError(
                "LLM returned invalid JSON."
            )