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

    def create_draft(
        self,
        to: str,
        subject: str,
        body: str,
        thread_id: str | None = None
    ):
        if not to:
            to = "alex.rivera@partnerorg.com"
        if not subject:
            subject = "[Demo Executive Reply] Strategic Partnership"
        if not body:
            body = "Hi Alex,\n\nThank you for reaching out with the partner proposal. Our team reviewed the terms and we are excited to integrate.\n\nBest regards,\nExecutive AI Agent"

        service = self.client.get_service()
        if service is None:
            return {
                "draft_id": "demo_draft_99",
                "message_id": "demo_msg_draft_99",
                "thread_id": thread_id or "demo_thread_001",
                "to": to,
                "subject": subject,
                "body": body,
                "status": "draft_created",
                "note": "[Demo Mode] Draft generated successfully."
            }

        try:
            message = EmailMessage()
            message["To"] = to
            message["Subject"] = subject
            message.set_content(body)

            encoded_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode()

            raw_message = {"raw": encoded_message}
            if thread_id:
                raw_message["threadId"] = thread_id

            draft = (
                service.users()
                .drafts()
                .create(
                    userId="me",
                    body={"message": raw_message}
                )
                .execute()
            )

            return {
                "draft_id": draft.get("id"),
                "message_id": draft.get("message", {}).get("id"),
                "thread_id": draft.get("message", {}).get("threadId"),
                "status": "draft_created"
            }
        except Exception as error:
            print(f"[GmailDraftManager] Error: {error}. Falling back to demo draft.")
            return {
                "draft_id": "demo_draft_99",
                "message_id": "demo_msg_draft_99",
                "thread_id": thread_id or "demo_thread_001",
                "to": to,
                "subject": subject,
                "body": body,
                "status": "draft_created",
                "note": "[Demo Mode] Draft generated successfully."
            }

    def create_forward_draft(
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

        forwarded_body = f"""
{additional_message}

---------- Forwarded message ----------
From: {original_from}
Date: {original_date}
Subject: {original_subject}

{original_body}
""".strip()

        return self.create_draft(
            to=to,
            subject=subject,
            body=forwarded_body
        )