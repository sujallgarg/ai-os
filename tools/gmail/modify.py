"""
Gmail message modification tools.

Currently supports marking messages as read or unread.
"""

from tools.gmail.client import GmailClient


class GmailModifier:

    def __init__(self):

        self.client = GmailClient()

        self.service = self.client.get_service()

    def mark_as_read(
        self,
        message_id: str
    ):

        self._validate_message_id(
            message_id
        )

        body = {
            "removeLabelIds": [
                "UNREAD"
            ]
        }

        return (
            self.service.users()
            .messages()
            .modify(
                userId="me",
                id=message_id,
                body=body
            )
            .execute()
        )

    def mark_as_unread(
        self,
        message_id: str
    ):

        self._validate_message_id(
            message_id
        )

        body = {
            "addLabelIds": [
                "UNREAD"
            ]
        }

        return (
            self.service.users()
            .messages()
            .modify(
                userId="me",
                id=message_id,
                body=body
            )
            .execute()
        )

    def _validate_message_id(
        self,
        message_id: str
    ):

        if not message_id:

            raise ValueError(
                "message_id is required."
            )