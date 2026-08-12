from tools.gmail.modify import GmailModifier


modifier = GmailModifier()

message_id = input(
    "Enter Gmail message ID to archive: "
)

modifier.archive(
    message_id
)

print(
    "Email archived successfully."
)
