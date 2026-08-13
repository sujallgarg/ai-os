"""
Gmail Send Manager.

Handles sending new emails and replies.
"""

import base64

from email.message import EmailMessage

from tools.gmail.client import GmailClient


class GmailSender:

    def __init__(self):

        self.client = GmailClient()

        self.service = self.client.get_service()

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        thread_id: str | None = None,
        in_reply_to: str | None = None,
        references: str | None = None
    ):

        self._validate(
            to,
            subject,
            body
        )

        message = EmailMessage()

        message["To"] = to
        message["Subject"] = subject

        if in_reply_to:

            message["In-Reply-To"] = in_reply_to

        if references:

            message["References"] = references

        message.set_content(body)

        encoded_message = (
            base64.urlsafe_b64encode(
                message.as_bytes()
            )
            .decode()
        )

        raw_message = {
            "raw": encoded_message
        }

        if thread_id:

            raw_message["threadId"] = thread_id

        result = (
            self.service.users()
            .messages()
            .send(
                userId="me",
                body=raw_message
            )
            .execute()
        )

        return {
            "status": "sent",
            "message_id": result.get("id"),
            "thread_id": result.get("threadId")
        }

    def reply_to_thread(
        self,
        to: str,
        subject: str,
        body: str,
        thread_id: str,
        in_reply_to: str | None = None,
        references: str | None = None
    ):

        if not thread_id:

            raise ValueError(
                "thread_id is required for a reply."
            )

        if not in_reply_to:

            raise ValueError(
                "in_reply_to is required for a reply."
            )

        return self.send_email(
            to=to,
            subject=subject,
            body=body,
            thread_id=thread_id,
            in_reply_to=in_reply_to,
            references=references
        )

    def _validate(
        self,
        to: str,
        subject: str,
        body: str
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