"""
Email Workflow Engine.

Determines what should happen after an email
has been classified.
"""

from workflow.rules import RuleEvaluator


class WorkflowEngine:

    def __init__(self):

        self.evaluator = RuleEvaluator()

        self.workflows = []

    def add_workflow(
        self,
        workflow
    ):

        self.workflows.append(
            workflow
        )

    def evaluate(
        self,
        email,
        classification
    ):

        matched_workflows = []

        for workflow in self.workflows:

            if not workflow.enabled:

                continue

            matches = self.evaluator.matches(
                workflow.conditions,
                classification
            )

            if matches:

                matched_workflows.append(
                    {
                        "workflow": workflow.name,
                        "action": workflow.action,
                        "action_config": workflow.action_config
                    }
                )

        return matched_workflows