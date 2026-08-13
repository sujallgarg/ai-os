from tools.gmail.attachments import GmailAttachmentManager


manager = GmailAttachmentManager()


message_id = input(
    "Enter Gmail message ID: "
)


attachments = manager.list_attachments(
    message_id
)


print("\nATTACHMENTS")
print("=" * 60)


if not attachments:

    print(
        "No attachments found."
    )

else:

    for index, attachment in enumerate(
        attachments,
        start=1
    ):

        print(
            f"{index}. "
            f"{attachment['filename']}"
        )

        print(
            "   Type:",
            attachment["mime_type"]
        )

        print(
            "   Size:",
            attachment["size"],
            "bytes"
        )

        print(
            "   ID:",
            attachment["attachment_id"]
        )

        print("-" * 60)
        