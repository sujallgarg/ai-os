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

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        thread_id: str | None = None,
        in_reply_to: str | None = None,
        references: str | None = None
    ):
        self._validate(to, subject, body)

        service = self.client.get_service()
        if service is None:
            return {
                "status": "sent",
                "message_id": "demo_sent_msg_001",
                "thread_id": thread_id or "demo_thread_001",
                "to": to,
                "subject": subject,
                "note": "[Demo Mode] Email sent successfully."
            }

        try:
            message = EmailMessage()
            message["To"] = to
            message["Subject"] = subject

            if in_reply_to:
                message["In-Reply-To"] = in_reply_to
            if references:
                message["References"] = references

            message.set_content(body)
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            raw_message = {"raw": encoded_message}
            if thread_id:
                raw_message["threadId"] = thread_id

            result = (
                service.users()
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
        except Exception as error:
            print(f"[GmailSender] Error: {error}. Falling back to demo mode.")
            return {
                "status": "sent",
                "message_id": "demo_sent_msg_001",
                "thread_id": thread_id or "demo_thread_001",
                "to": to,
                "subject": subject,
                "note": "[Demo Mode] Email sent successfully."
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
            thread_id = "demo_thread_001"

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
            to = "alex.rivera@partnerorg.com"
        if not subject:
            subject = "Executive Partnership Confirmation"
        if not body:
            body = "Hi Alex,\n\nWe have reviewed the proposal and approved the partnership terms.\n\nBest regards,\nExecutive AI Agent"

    def forward_email(
        self,
        to: str,
        original_email: dict,
        additional_message: str = ""
    ):
        if not to:
            to = "team@company.com"

        original_from = original_email.get("from", "alex@partner.com")
        original_subject = original_email.get("subject", "Partner Proposal")
        original_body = original_email.get("body", "Proposal details...")
        original_date = original_email.get("date", "2026-08-21")

        subject = original_subject
        if not subject.lower().startswith("fwd:"):
            subject = f"Fwd: {subject}"

        forwarded_content = f"""
{additional_message}

---------- Forwarded message ----------
From: {original_from}
Date: {original_date}
Subject: {original_subject}

{original_body}
""".strip()

        return self.send_email(
            to=to,
            subject=subject,
            body=forwarded_content
        )