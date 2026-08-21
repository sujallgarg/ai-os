"""
Gmail Search Tool
Searches a user's Gmail mailbox using Gmail search syntax.
"""

from tools.gmail.client import GmailClient


LABEL_QUERIES = {
    "important": "is:important",
    "starred": "is:starred",
    "unread": "is:unread",
    "sent": "in:sent",
    "draft": "in:drafts",
    "trash": "in:trash",
    "spam": "in:spam",
    "inbox": "in:inbox"
}


class GmailSearcher:

    def __init__(self):
        self.client = GmailClient()

    def search(self, query: str, limit: int = 10):
        if not query or not query.strip():
            query = "proposal"

        service = self.client.get_service()
        if service is None:
            return [
                {
                    "id": "demo_search_01",
                    "thread_id": "demo_thread_001",
                    "from": "Alex Rivera <alex.rivera@partnerorg.com>",
                    "to": "me",
                    "subject": f"[Demo Match for '{query}'] Partner Proposal & API Access",
                    "date": "Fri, 21 Aug 2026 14:00:00 GMT",
                    "snippet": "We reviewed your AI platform and would love to move forward with executive replies..."
                }
            ]

        try:
            results = (
                service.users()
                .messages()
                .list(
                    userId="me",
                    q=query,
                    maxResults=limit
                )
                .execute()
            )

            messages = results.get("messages", [])
            emails = []

            for message in messages:
                email = (
                    service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=message["id"],
                        format="metadata",
                        metadataHeaders=["From", "To", "Subject", "Date"]
                    )
                    .execute()
                )

                headers = email.get("payload", {}).get("headers", [])
                header_data = {}

                for header in headers:
                    header_data[header["name"].lower()] = header["value"]

                emails.append({
                    "id": message["id"],
                    "thread_id": email.get("threadId"),
                    "from": header_data.get("from", ""),
                    "to": header_data.get("to", ""),
                    "subject": header_data.get("subject", ""),
                    "date": header_data.get("date", ""),
                    "snippet": email.get("snippet", "")
                })

            return emails
        except Exception as error:
            print(f"[GmailSearcher] Error: {error}. Falling back to demo mode.")
            return [
                {
                    "id": "demo_search_01",
                    "thread_id": "demo_thread_001",
                    "from": "Alex Rivera <alex.rivera@partnerorg.com>",
                    "to": "me",
                    "subject": f"[Demo Match for '{query}'] Partner Proposal & API Access",
                    "date": "Fri, 21 Aug 2026 14:00:00 GMT",
                    "snippet": "We reviewed your AI platform and would love to move forward with executive replies..."
                }
            ]

    def search_by_label(self, label: str, limit: int = 10):
        query = LABEL_QUERIES.get(label.lower(), "is:unread")
        return self.search(query=query, limit=limit)