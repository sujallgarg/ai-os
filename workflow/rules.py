"""
Workflow rule evaluation.
"""


class RuleEvaluator:

    def matches(
        self,
        conditions: dict,
        classification: dict
    ):

        for key, expected_value in conditions.items():

            actual_value = classification.get(
                key
            )

            if actual_value != expected_value:

                return False

        return True