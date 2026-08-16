"""
AI Task Planner.

Converts natural-language user requests into
structured execution plans.
"""

import json
import re

from llm.provider import LLMProvider

from planner.models import (
    PlanStep,
    TaskPlan
)

from planner.validator import (
    PlanValidator
)


class TaskPlanner:

    def __init__(self):

        self.llm = LLMProvider()

        self.validator = (
            PlanValidator()
        )

    def create_plan(
        self,
        user_request: str,
        memories: list | None = None
    ):

        if not user_request:

            raise ValueError(
                "User request is required."
            )

        memories = memories or []

        memory_context = "\n".join(
            str(memory)
            for memory in memories
        )

        prompt = f"""
You are the task planner for an AI operating system.

Convert the user's request into a structured execution plan.

USER REQUEST:
{user_request}

RELEVANT USER MEMORY:
{memory_context}

AVAILABLE AGENTS:

- email
- browser
- coding
- calendar
- file

Rules:

1. Break complex requests into small steps.
2. Each step must have one agent.
3. Each step must have one action.
4. Use dependencies when one step requires another.
5. Do not invent unavailable agents.
6. Return ONLY valid JSON.

Return:

{{
    "goal": "short description",
    "steps": [
        {{
            "id": 1,
            "description": "what to do",
            "agent": "email",
            "action": "search",
            "parameters": {{}},
            "depends_on": []
        }}
    ]
}}
"""

        messages = [

            {
                "role": "system",
                "content": (
                    "You are a task planning "
                    "engine. Return valid JSON only."
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

        plan = self._parse_response(
            response
        )

        self.validator.validate(
            plan
        )

        return self._build_plan(
            plan
        )

    def _parse_response(
        self,
        response
    ):

        if isinstance(
            response,
            dict
        ):

            return response

        if not response or not isinstance(response, str):

            raise ValueError(
                "Planner received empty or invalid response from LLM."
            )

        clean_text = response.strip()

        # Remove markdown code fences if present
        if "```" in clean_text:
            clean_text = re.sub(r"^```(?:json)?\s*", "", clean_text)
            clean_text = re.sub(r"\s*```$", "", clean_text)
            clean_text = clean_text.strip()

        # 1. Try direct parse
        try:
            return json.loads(clean_text)
        except json.JSONDecodeError:
            pass

        # 2. Try regex extraction of JSON object
        match = re.search(r"\{[\s\S]*\}", clean_text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass

        raise ValueError(
            "Planner returned invalid JSON."
        )

    def _build_plan(
        self,
        plan: dict
    ):

        steps = []

        for raw_step in plan["steps"]:

            steps.append(
                PlanStep(

                    id=raw_step["id"],

                    description=(
                        raw_step["description"]
                    ),

                    agent=raw_step["agent"],

                    action=raw_step["action"],

                    parameters=(
                        raw_step.get(
                            "parameters",
                            {}
                        )
                    ),

                    depends_on=(
                        raw_step.get(
                            "depends_on",
                            []
                        )
                    )
                )
            )

        return TaskPlan(

            goal=plan["goal"],

            steps=steps
        )