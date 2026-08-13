from workflow.model import WorkflowRule


EMAIL_WORKFLOWS = [

    WorkflowRule(

        name="Urgent Email Alert",

        conditions={
            "priority": "urgent"
        },

        action="notify_user"
    ),

    WorkflowRule(

        name="Client Reply",

        conditions={
            "category": "client",
            "requires_reply": True
        },

        action="draft_reply",

        action_config={
            "tone": "professional"
        }
    ),

    WorkflowRule(

        name="Ignore Newsletters",

        conditions={
            "category": "newsletter",
            "requires_reply": False
        },

        action="ignore"
    )
]