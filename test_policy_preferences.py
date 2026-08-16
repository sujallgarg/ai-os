from policy.engine import PolicyEngine


engine = PolicyEngine()


result = engine.evaluate(

    action="send_email",

    context={
        "category": "client",
        "priority": "low"
    }
)


print("\nCLIENT EMAIL")
print("=" * 60)

print(
    "Decision:",
    result.decision
)

print(
    "Reason:",
    result.reason
)

print(
    "Approval:",
    result.requires_approval
)