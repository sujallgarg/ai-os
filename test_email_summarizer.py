from tools.gmail.read import GmailReader

from agents.email.summarize import EmailSummarizer


reader = GmailReader()

summarizer = EmailSummarizer()

emails = reader.get_unread_messages(limit=10)

summary = summarizer.summarize(emails)

print("\n")
print("=" * 60)
print("AI EMAIL SUMMARY")
print("=" * 60)
print(summary)