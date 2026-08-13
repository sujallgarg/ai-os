from security.approval import ApprovalManager


approval = ApprovalManager()


action = "send_email"


if approval.requires_approval(action):

    request = approval.create_request(
        action=action,
        description="Send email to John",
        data={
            "to": "john@example.com",
            "subject": "Project Update"
        }
    )

    print(
        "Approval required:"
    )

    print(request)

else:

    print(
        "No approval required."
    )