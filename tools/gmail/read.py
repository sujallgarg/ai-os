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

    def get_unread_messages(self, limit=10):
        service = self.client.get_service()
        if service is None:
            # Demo mode fallback
            return [
                {
                    "id": "demo_msg_001",
                    "thread_id": "demo_thread_001",
                    "subject": "[Demo] Strategic Partnership & Integration Proposal",
                    "from": "Alex Rivera <alex.rivera@partnerorg.com>",
                    "snippet": "Hi Team, we reviewed your AI platform and would love to explore a joint executive integration. Attached is our proposal..."
                },
                {
                    "id": "demo_msg_002",
                    "thread_id": "demo_thread_002",
                    "subject": "[Demo] Enterprise SaaS Expansion Inquiry",
                    "from": "Sarah Chen <sarah@enterprise-saas.io>",
                    "snippet": "Hello, we are interested in deploying your autonomous agent workspace across our 50-person engineering team..."
                }
            ]

        try:
            results = service.users().messages().list(
                userId="me",
                labelIds=["UNREAD"],
                maxResults=limit
            ).execute()

            messages = results.get("messages", [])
            emails = []

            for msg in messages:
                message = service.users().messages().get(
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
                    "thread_id": message.get("threadId", msg.get("threadId", "")),
                    "subject": _clean(subject),
                    "from": _clean(sender),
                    "snippet": _clean(snippet)
                })

            return emails
        except Exception as error:
            print(f"[GmailReader] Error: {error}. Falling back to demo mode.")
            return self.get_unread_messages(limit=limit)

    get_unread_emails = get_unread_messages