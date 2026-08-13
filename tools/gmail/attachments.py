"""
Gmail Attachment Manager.

Lists and downloads attachments from Gmail messages.
"""

import base64
from pathlib import Path

from tools.gmail.client import GmailClient


class GmailAttachmentManager:

    def __init__(self):

        self.client = GmailClient()

        self.service = self.client.get_service()

    def list_attachments(
        self,
        message_id: str
    ):

        if not message_id:
            raise ValueError(
                "message_id is required."
            )

        message = (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full"
            )
            .execute()
        )

        attachments = []

        self._find_attachments(
            message.get("payload", {}),
            attachments
        )

        return attachments

    def _find_attachments(
        self,
        part,
        attachments
    ):

        filename = part.get(
            "filename"
        )

        body = part.get(
            "body",
            {}
        )

        attachment_id = body.get(
            "attachmentId"
        )

        if filename and attachment_id:

            attachments.append({
                "filename": filename,
                "mime_type": part.get(
                    "mimeType",
                    "application/octet-stream"
                ),
                "attachment_id": attachment_id,
                "size": body.get(
                    "size",
                    0
                )
            })

        for child in part.get(
            "parts",
            []
        ):

            self._find_attachments(
                child,
                attachments
            )

    def download_attachment(
        self,
        message_id: str,
        attachment_id: str,
        filename: str,
        output_dir: str = "data/attachments"
    ):

        if not message_id:
            raise ValueError(
                "message_id is required."
            )

        if not attachment_id:
            raise ValueError(
                "attachment_id is required."
            )

        response = (
            self.service.users()
            .messages()
            .attachments()
            .get(
                userId="me",
                messageId=message_id,
                id=attachment_id
            )
            .execute()
        )

        data = response.get(
            "data",
            ""
        )

        decoded = base64.urlsafe_b64decode(
            data + "=" * (-len(data) % 4)
        )

        directory = Path(
            output_dir
        )

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        safe_filename = Path(
            filename
        ).name

        output_path = (
            directory / safe_filename
        )

        output_path.write_bytes(
            decoded
        )

        return {
            "filename": safe_filename,
            "path": str(output_path),
            "size": len(decoded)
        }