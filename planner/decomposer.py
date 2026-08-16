"""
Task Decomposer.

Breaks high-level plan steps into smaller
executable tasks.
"""

import json
import re

from llm.provider import LLMProvider

from planner.models import (
    PlanStep,
    ExecutionTask
)


class TaskDecomposer:

    def __init__(self):

        self.llm = LLMProvider()

    def decompose(
        self,
        step: PlanStep
    ):

        if not step:

            raise ValueError(
                "Plan step is required."
            )

        prompt = f"""
You are a task decomposition engine.

Break the following high-level task into
small, executable tasks.

HIGH-LEVEL TASK:

Description:
{step.description}

Agent:
{step.agent}

Action:
{step.action}

Parameters:
{json.dumps(step.parameters)}

Rules:

1. Break the task into practical steps.
2. Keep each task small.
3. Every task must have an agent.
4. Every task must have an action.
5. Preserve the original objective.
6. Do not invent unavailable agents.
7. Return ONLY valid JSON.

Available agents:

- email
- browser
- coding
- calendar
- file

Return:

{{
    "tasks": [
        {{
            "id": 1,
            "description": "task description",
            "agent": "{step.agent}",
            "action": "action_name",
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
                    "You are a task decomposition "
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

        data = self._parse_response(
            response
        )

        return self._build_tasks(
            data
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
                "Decomposer received empty or invalid response from LLM."
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
            "Decomposer returned invalid JSON."
        )

    def _build_tasks(
        self,
        data: dict
    ):

        raw_tasks = data.get(
            "tasks",
            []
        )

        tasks = []

        for raw_task in raw_tasks:

            tasks.append(
                ExecutionTask(

                    id=raw_task["id"],

                    description=(
                        raw_task["description"]
                    ),

                    agent=raw_task["agent"],

                    action=raw_task["action"],

                    parameters=(
                        raw_task.get(
                            "parameters",
                            {}
                        )
                    ),

                    depends_on=(
                        raw_task.get(
                            "depends_on",
                            []
                        )
                    ),

                    status="pending"
                )
            )

        return tasks