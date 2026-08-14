"""
AI Email Classifier.

Classifies emails based on their content and determines
whether they require user attention or a reply.
"""

import json
import re

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
            messages,
            response_format={"type": "json_object"}
        )

        return self._parse_response(
            response
        )

    def _parse_response(
        self,
        response
    ):

        if isinstance(response, dict):

            return self._normalize_result(response)

        if not response or not isinstance(response, str):

            return self._default_classification(
                reason="Empty or invalid response from LLM."
            )

        clean_text = response.strip()

        # Remove markdown code blocks if wrapped in ```json ... ```
        if "```" in clean_text:
            clean_text = re.sub(r"^```(?:json)?\s*", "", clean_text)
            clean_text = re.sub(r"\s*```$", "", clean_text)
            clean_text = clean_text.strip()

        # 1. Try direct json.loads
        try:
            parsed = json.loads(clean_text)
            if isinstance(parsed, dict):
                return self._normalize_result(parsed)
        except json.JSONDecodeError:
            pass

        # 2. Try regex extraction of JSON object {...}
        match = re.search(r"\{[\s\S]*\}", clean_text)
        if match:
            try:
                parsed = json.loads(match.group(0))
                if isinstance(parsed, dict):
                    return self._normalize_result(parsed)
            except json.JSONDecodeError:
                pass

        # 3. Fallback default classification if all parsing fails
        return self._default_classification(
            reason="Failed to parse LLM JSON output."
        )

    def _normalize_result(
        self,
        data: dict
    ) -> dict:

        def to_bool(val):
            if isinstance(val, bool):
                return val
            if isinstance(val, str):
                return val.strip().lower() in ("true", "1", "yes")
            return bool(val)

        return {
            "category": str(data.get("category", "other")).lower().strip(),
            "priority": str(data.get("priority", "low")).lower().strip(),
            "requires_reply": to_bool(data.get("requires_reply", False)),
            "requires_action": to_bool(data.get("requires_action", False)),
            "sentiment": str(data.get("sentiment", "neutral")).lower().strip(),
            "reason": str(data.get("reason", "")).strip()
        }

    def _default_classification(
        self,
        reason: str = ""
    ) -> dict:

        return {
            "category": "notification",
            "priority": "low",
            "requires_reply": False,
            "requires_action": False,
            "sentiment": "neutral",
            "reason": reason or "Default fallback classification"
        }