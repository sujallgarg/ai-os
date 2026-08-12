from tools.gmail.read import GmailReader

reader = GmailReader()

emails = reader.get_unread_messages()

for email in emails:

    print("=" * 50)

    print("ID:", email.get("id"))
    print("THREAD ID:", email.get("thread_id"))
    print("FROM:", email["from"])
    print("SUBJECT:", email["subject"])
    print("SNIPPET:", email["snippet"])