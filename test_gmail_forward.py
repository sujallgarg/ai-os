from tools.gmail.body import GmailBodyReader
from tools.gmail.draft import GmailDraftManager


reader = GmailBodyReader()

draft_manager = GmailDraftManager()


message_id = input(
    "Enter message ID to forward: "
)

recipient = input(
    "Forward to: "
)

additional_message = input(
    "Message to include: "
)


original_email = reader.get_email(
    message_id
)


draft = draft_manager.create_forward_draft(
    to=recipient,
    original_email=original_email,
    additional_message=additional_message
)


print("\n")
print("=" * 60)

print("FORWARDED DRAFT CREATED")

print("=" * 60)

print(draft)

print("=" * 60)