"""
Validates AI-generated task plans.
"""


ALLOWED_AGENTS = {
    "email",
    "browser",
    "coding",
    "calendar",
    "file"
}


class PlanValidator:

    def validate(
        self,
        plan: dict
    ):

        if not isinstance(
            plan,
            dict
        ):

            raise ValueError(
                "Plan must be a dictionary."
            )

        if not plan.get("goal"):

            raise ValueError(
                "Plan goal is required."
            )

        steps = plan.get(
            "steps"
        )

        if not isinstance(
            steps,
            list
        ):

            raise ValueError(
                "Plan steps must be a list."
            )

        for step in steps:

            if not step.get("agent"):

                raise ValueError(
                    "Every step requires an agent."
                )

            if (
                step["agent"]
                not in ALLOWED_AGENTS
            ):

                raise ValueError(
                    f"Unknown agent: "
                    f"{step['agent']}"
                )

            if not step.get("action"):

                raise ValueError(
                    "Every step requires an action."
                )

        return True