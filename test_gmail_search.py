from tools.gmail.search import GmailSearcher


searcher = GmailSearcher()

emails = searcher.search(
    "is:unread",
    limit=10
)

for email in emails:

    print("=" * 60)

    print("ID:", email["id"])
    print("THREAD ID:", email.get("thread_id"))
    print("FROM:", email["from"])
    print("SUBJECT:", email["subject"])
    print("DATE:", email["date"])
    print("SNIPPET:", email["snippet"])