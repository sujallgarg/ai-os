from policy.engine import PolicyEngine


engine = PolicyEngine()


tests = [

    {
        "action": "summarize_email",
        "context": {}
    },

    {
        "action": "send_email",
        "context": {}
    },

    {
        "action": "delete_file",
        "context": {}
    },

    {
        "action": "draft_reply",
        "context": {
            "category": "client",
            "priority": "medium"
        }
    },

    {
        "action": "send_email",
        "context": {
            "category": "finance"
        }
    }
]


for test in tests:

    result = engine.evaluate(
        action=test["action"],
        context=test["context"]
    )

    print("\n")
    print("=" * 60)

    print(
        "ACTION:",
        result.action
    )

    print(
        "DECISION:",
        result.decision
    )

    print(
        "REASON:",
        result.reason
    )

    print(
        "APPROVAL:",
        result.requires_approval
    )