from workflow.engine import WorkflowEngine

from config.email_workflows import EMAIL_WORKFLOWS


engine = WorkflowEngine()


for workflow in EMAIL_WORKFLOWS:

    engine.add_workflow(
        workflow
    )


email = {

    "from": "client@example.com",

    "subject": "Project Update",

    "body": "Can you send the proposal?"
}


classification = {

    "category": "client",

    "priority": "high",

    "requires_reply": True,

    "requires_action": True
}


results = engine.evaluate(
    email=email,
    classification=classification
)


print("\nMATCHED WORKFLOWS")
print("=" * 60)


for result in results:

    print(
        "Workflow:",
        result["workflow"]
    )

    print(
        "Action:",
        result["action"]
    )

    print(
        "Config:",
        result["action_config"]
    )

    print("-" * 60)