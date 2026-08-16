from planner.planner import TaskPlanner


planner = TaskPlanner()


request = """
Check my email for the latest client message
about the proposal and draft a professional reply.
"""


plan = planner.create_plan(
    user_request=request
)


print("\nTASK PLAN")
print("=" * 70)

print(
    "GOAL:",
    plan.goal
)


for step in plan.steps:

    print("\nSTEP", step.id)

    print(
        "Description:",
        step.description
    )

    print(
        "Agent:",
        step.agent
    )

    print(
        "Action:",

        step.action
    )

    print(
        "Parameters:",
        step.parameters
    )

    print(
        "Depends on:",
        step.depends_on
    )