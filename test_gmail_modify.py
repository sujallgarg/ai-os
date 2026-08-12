from tools.gmail.modify import GmailModifier


modifier = GmailModifier()


message_id = input(
    "Enter Gmail message ID: "
)


print("\nChoose action:")

print("1. Mark as read")
print("2. Mark as unread")


choice = input(
    "\nChoice: "
)


if choice == "1":

    result = modifier.mark_as_read(
        message_id
    )

    print(
        "\nEmail marked as read."
    )


elif choice == "2":

    result = modifier.mark_as_unread(
        message_id
    )

    print(
        "\nEmail marked as unread."
    )


else:

    print(
        "\nInvalid choice."
    )
    