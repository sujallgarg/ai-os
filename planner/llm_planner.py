import json

from planner.models import (
    TaskPlan
)

from planner.prompt import (
    SYSTEM_PROMPT
)


class LLMPlanner:

    def __init__(
        self,
        client,
        model: str
    ):

        self.client = client

        self.model = model


    async def plan(
        self,
        goal: str
    ) -> TaskPlan:

        response = await self.client.responses.create(

            model=self.model,

            input=[

                {
                    "role": "system",

                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",

                    "content": (
                        "Create an execution plan "
                        "for this goal:\n\n"
                        f"{goal}"
                    )
                }
            ],

            text={
                "format": {
                    "type": "json_schema",

                    "name": "task_plan",

                    "schema": TaskPlan.model_json_schema(),

                    "strict": True
                }
            }
        )

        raw_output = (
            response.output_text
        )

        data = json.loads(
            raw_output
        )

        return TaskPlan.model_validate(
            data
        )