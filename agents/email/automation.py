"""
Email Automation Agent.

Connects email classification with the
workflow engine.
"""

from workflow.engine import WorkflowEngine

from config.email_workflows import EMAIL_WORKFLOWS


class EmailAutomationAgent:

    def __init__(self):

        self.workflow_engine = WorkflowEngine()

        for workflow in EMAIL_WORKFLOWS:

            self.workflow_engine.add_workflow(
                workflow
            )

    def process(
        self,
        email,
        classification
    ):

        return self.workflow_engine.evaluate(
            email=email,
            classification=classification
        )