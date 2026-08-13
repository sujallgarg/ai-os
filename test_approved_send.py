from security.approval import ApprovalManager
from execution.action_executor import ActionExecutor


approval = ApprovalManager()

executor = ActionExecutor()


request = approval.create_request(

    action="send_email",

    description="Send project update",

    data={
        "to": "test@example.com",

        "subject": "Project Update",

        "body": (
            "Hi,\n\n"
            "I'll send the report tomorrow.\n\n"
            "Thanks."
        )
    }
)


print("Request created:")

print(request)


choice = input(
    "\nApprove send? Type YES: "
)


if choice != "YES":

    approval.reject(request)

    print(
        "Email was NOT sent."
    )

    raise SystemExit


approval.approve(request)


result = executor.execute(
    request
)


print("\nResult:")

print(result)
