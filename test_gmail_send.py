from tools.gmail.send import GmailSender


sender = GmailSender()


to = input(
    "Recipient email: "
)

subject = input(
    "Subject: "
)

body = input(
    "Email body: "
)


confirmation = input(
    "\nType SEND to actually send: "
)


if confirmation != "SEND":

    print(
        "Send cancelled."
    )

    raise SystemExit


result = sender.send_email(
    to=to,
    subject=subject,
    body=body
)


print("\nEmail sent.")

print(
    "Message ID:",
    result["message_id"]
)

print(
    "Thread ID:",
    result["thread_id"]
)