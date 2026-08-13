from tools.gmail.send import GmailSender


sender = GmailSender()


to = input(
    "Recipient email: "
)

subject = input(
    "Reply subject: "
)

body = input(
    "Reply body: "
)

thread_id = input(
    "Thread ID: "
)

in_reply_to = input(
    "Message ID being replied to: "
)


print("\n")

confirmation = input(
    "Type SEND to send this reply: "
)


if confirmation != "SEND":

    print(
        "Reply cancelled."
    )

    raise SystemExit


result = sender.reply_to_thread(
    to=to,
    subject=subject,
    body=body,
    thread_id=thread_id,
    in_reply_to=in_reply_to
)


print("\nReply sent successfully.")

print(
    "Message ID:",
    result["message_id"]
)

print(
    "Thread ID:",
    result["thread_id"]
)