from tools.gmail.search import GmailSearcher


searcher = GmailSearcher()


emails = searcher.search_by_label(
    "important",
    limit=10
)


print("\nIMPORTANT EMAILS")
print("=" * 60)


for email in emails:

    print(
        email["from"]
    )

    print(
        email["subject"]
    )

    print(
        email["snippet"]
    )

    print("-" * 60)
