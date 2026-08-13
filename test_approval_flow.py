from security.approval import ApprovalManager


approval = ApprovalManager()


request = approval.create_request(
    action="send_email",
    description="Send project update to John",
    data={
        "to": "john@example.com",
        "subject": "Project Update"
    }
)


print("Initial request:")
print(request)


approved = approval.approve(
    request
)


print("\nAfter approval:")
print(approved)