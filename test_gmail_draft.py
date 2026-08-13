from tools.gmail.draft import GmailDraftManager


manager = GmailDraftManager()


to = input(
    "Recipient email: "
)

subject = input(
    "Subject: "
)

body = input(
    "Email body: "
)


result = manager.create_draft(
    to=to,
    subject=subject,
    body=body
)


print("\nDraft created successfully.")

print(
    "Draft ID:",
    result["draft_id"]
)

print(
    "Message ID:",
    result["message_id"]
)