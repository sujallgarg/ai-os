"""
Gmail Full Email Body Reader.
Retrieves the complete content of a Gmail message and handles plain-text and HTML MIME parts.
"""

import base64
import re
from tools.gmail.client import GmailClient


class GmailBodyReader:

    def __init__(self):
        self.client = GmailClient()

    def get_email(self, message_id: str):
        if not message_id:
            message_id = "demo_msg_001"

        service = self.client.get_service()
        if service is None:
            return {
                "id": message_id,
                "thread_id": "demo_thread_001",
                "from": "Alex Rivera <alex.rivera@partnerorg.com>",
                "to": "me",
                "cc": "",
                "subject": "[Demo] Strategic Partnership & Integration Proposal",
                "date": "Fri, 21 Aug 2026 14:00:00 GMT",
                "body": "Hi Team,\n\nWe reviewed your AI platform and would love to explore a joint executive integration. Attached is our proposal outline.\n\nBest,\nAlex",
                "snippet": "We reviewed your AI platform and would love to explore a joint executive integration..."
            }

        try:
            message = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                    format="full"
                )
                .execute()
            )

            payload = message.get("payload", {})
            headers = self._get_headers(payload)
            body = self._extract_body(payload)

            return {
                "id": message.get("id"),
                "thread_id": message.get("threadId"),
                "from": headers.get("from", ""),
                "to": headers.get("to", ""),
                "cc": headers.get("cc", ""),
                "subject": headers.get("subject", ""),
                "date": headers.get("date", ""),
                "body": body,
                "snippet": message.get("snippet", "")
            }
        except Exception as error:
            print(f"[GmailBodyReader] Error: {error}. Falling back to demo mode.")
            return {
                "id": message_id,
                "thread_id": "demo_thread_001",
                "from": "Alex Rivera <alex.rivera@partnerorg.com>",
                "to": "me",
                "cc": "",
                "subject": "[Demo] Strategic Partnership & Integration Proposal",
                "date": "Fri, 21 Aug 2026 14:00:00 GMT",
                "body": "Hi Team,\n\nWe reviewed your AI platform and would love to explore a joint executive integration. Attached is our proposal outline.\n\nBest,\nAlex",
                "snippet": "We reviewed your AI platform and would love to explore a joint executive integration..."
            }

    def _get_headers(self, payload):
        headers = {}
        for header in payload.get("headers", []):
            name = header.get("name", "").lower()
            value = header.get("value", "")
            headers[name] = value
        return headers

    def _extract_body(self, payload):
        mime_type = payload.get("mimeType", "")
        body_data = payload.get("body", {}).get("data")
        if body_data:
            return self._decode_body(body_data)

        parts = payload.get("parts", [])
        plain_text = None
        html_text = None

        for part in parts:
            part_type = part.get("mimeType", "")
            part_body = part.get("body", {})
            data = part_body.get("data")
            if data:
                decoded = self._decode_body(data)
                if part_type == "text/plain":
                    plain_text = decoded
                elif part_type == "text/html":
                    html_text = decoded

            if part.get("parts"):
                nested_body = self._extract_body(part)
                if nested_body:
                    if part_type == "text/plain":
                        plain_text = nested_body
                    elif part_type == "text/html":
                        html_text = nested_body

        if plain_text:
            return plain_text.strip()
        if html_text:
            return self._html_to_text(html_text)
        return ""

    def _decode_body(self, data):
        try:
            decoded = base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))
            return decoded.decode("utf-8", errors="replace")
        except Exception:
            return ""

    def _html_to_text(self, html):
        html = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
        html = re.sub(r"</p>", "\n\n", html, flags=re.IGNORECASE)
        html = re.sub(r"<[^>]+>", "", html)
        return html.strip()