import base64
import html
import re
from email.header import decode_header

from tools.gmail.client import GmailClient


def _clean(text: str) -> str:
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"[\ufeff\u200b\u200c\u200d\u034f]", "", text)
    return re.sub(r"\s+", " ", text).strip()


class GmailReader:

    def __init__(self):
        self.client = GmailClient()
        self.service = self.client.get_service()

    def get_unread_messages(self, limit=10):
        results = self.service.users().messages().list(
            userId="me",
            labelIds=["UNREAD"],
            maxResults=limit
        ).execute()

        messages = results.get("messages", [])
        emails = []

        for msg in messages:
            message = self.service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="full"
            ).execute()

            headers = message.get("payload", {}).get("headers", [])

            subject = ""
            sender = ""

            for header in headers:
                if header["name"] == "Subject":
                    subject = header["value"]
                elif header["name"] == "From":
                    sender = header["value"]

            snippet = message.get("snippet", "")

            emails.append({
                "id": msg["id"],
                "subject": _clean(subject),
                "from": _clean(sender),
                "snippet": _clean(snippet)
            })

        return emails