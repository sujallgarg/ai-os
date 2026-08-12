from tools.gmail.modify import GmailModifier


modifier = GmailModifier()


message_id = input(
    "Enter Gmail message ID to move to trash: "
)


modifier.move_to_trash(
    message_id
)


print(
    "Email moved to trash."
)
