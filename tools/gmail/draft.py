"""
Gmail Draft Manager.

Creates drafts in the user's Gmail account.

This module does NOT send emails.
"""

import base64

from email.message import EmailMessage

from tools.gmail.client import GmailClient


class GmailDraftManager:

    def __init__(self):

        self.client = GmailClient()

        self.service = self.client.get_service()

    def create_draft(
        self,
        to: str,
        subject: str,
        body: str,
        thread_id: str | None = None
    ):

        if not to:
            raise ValueError(
                "Recipient email is required."
            )

        if not subject:
            raise ValueError(
                "Email subject is required."
            )

        if not body:
            raise ValueError(
                "Email body is required."
            )

        message = EmailMessage()

        message["To"] = to

        message["Subject"] = subject

        message.set_content(body)

        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        raw_message = {
            "raw": encoded_message
        }

        if thread_id:

            raw_message["threadId"] = thread_id

        draft = (
            self.service.users()
            .drafts()
            .create(
                userId="me",
                body={
                    "message": raw_message
                }
            )
            .execute()
        )

        return {
            "draft_id": draft.get("id"),
            "message_id": draft.get(
                "message",
                {}
            ).get("id"),
            "thread_id": draft.get(
                "message",
                {}
            ).get("threadId")
        }
        