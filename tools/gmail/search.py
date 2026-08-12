"""
Gmail Search Tool

Searches a user's Gmail mailbox using Gmail search syntax.
"""

from tools.gmail.client import GmailClient


class GmailSearcher:

    def __init__(self):
        self.client = GmailClient()
        self.service = self.client.get_service()

    def search(self, query: str, limit: int = 10):

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        results = (
            self.service.users()
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
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=message["id"],
                    format="metadata",
                    metadataHeaders=[
                        "From",
                        "To",
                        "Subject",
                        "Date"
                    ]
                )
                .execute()
            )

            headers = email.get(
                "payload",
                {}
            ).get(
                "headers",
                []
            )

            header_data = {}

            for header in headers:

                header_data[
                    header["name"].lower()
                ] = header["value"]

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