"""
Gmail Thread Reader

Retrieves an entire Gmail conversation and converts
its messages into structured data for the AI agent.
"""

from tools.gmail.client import GmailClient
from tools.gmail.body import GmailBodyReader


class GmailThreadReader:

    def __init__(self):

        self.client = GmailClient()

        self.service = self.client.get_service()

        self.body_reader = GmailBodyReader()

    def get_thread(self, thread_id: str):
        if not thread_id or not str(thread_id).strip():
            raise ValueError("thread_id is required.")

        thread_id = str(thread_id).strip()


        thread = (
            self.service.users()
            .threads()
            .get(
                userId="me",
                id=thread_id,
                format="full"
            )
            .execute()
        )

        messages = thread.get(
            "messages",
            []
        )

        conversation = []

        for message in messages:

            message_id = message.get("id")

            email = self.body_reader.get_email(
                message_id
            )

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
        