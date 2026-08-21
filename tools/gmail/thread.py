"""
Gmail Thread Reader
Retrieves an entire Gmail conversation and returns the messages in a structured format.
"""

from tools.gmail.client import GmailClient
from tools.gmail.body import GmailBodyReader


class GmailThreadReader:

    def __init__(self):
        self.client = GmailClient()
        self.body_reader = GmailBodyReader()

    def get_thread(self, thread_id: str):
        if not thread_id:
            thread_id = "demo_thread_001"

        service = self.client.get_service()
        if service is None:
            return {
                "thread_id": thread_id,
                "message_count": 1,
                "messages": [
                    {
                        "id": "demo_msg_001",
                        "from": "Alex Rivera <alex.rivera@partnerorg.com>",
                        "to": "me",
                        "cc": "",
                        "subject": "[Demo] Strategic Partnership & Integration Proposal",
                        "date": "Fri, 21 Aug 2026 14:00:00 GMT",
                        "body": "Hi Team,\n\nWe reviewed your AI platform and would love to explore a joint executive integration. Attached is our proposal outline.\n\nBest,\nAlex"
                    }
                ]
            }

        try:
            thread = (
                service.users()
                .threads()
                .get(
                    userId="me",
                    id=thread_id,
                    format="full"
                )
                .execute()
            )

            messages = thread.get("messages", [])
            conversation = []

            for message in messages:
                message_id = message.get("id")
                email = self.body_reader.get_email(message_id)

                conversation.append({
                    "id": email.get("id"),
                    "from": email.get("from", ""),
                    "to": email.get("to", ""),
                    "cc": email.get("cc", ""),
                    "subject": email.get("subject", ""),
                    "date": email.get("date", ""),
                    "body": email.get("body", "")
                })

            return {
                "thread_id": thread_id,
                "message_count": len(conversation),
                "messages": conversation
            }
        except Exception as error:
            print(f"[GmailThreadReader] Error: {error}. Falling back to demo thread.")
            return {
                "thread_id": thread_id,
                "message_count": 1,
                "messages": [
                    {
                        "id": "demo_msg_001",
                        "from": "Alex Rivera <alex.rivera@partnerorg.com>",
                        "to": "me",
                        "cc": "",
                        "subject": "[Demo] Strategic Partnership & Integration Proposal",
                        "date": "Fri, 21 Aug 2026 14:00:00 GMT",
                        "body": "Hi Team,\n\nWe reviewed your AI platform and would love to explore a joint executive integration. Attached is our proposal outline.\n\nBest,\nAlex"
                    }
                ]
            }