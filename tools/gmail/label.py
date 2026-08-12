"""
Gmail Labels Manager.
"""

from tools.gmail.client import GmailClient


SYSTEM_LABELS = {

    "inbox": "INBOX",

    "sent": "SENT",

    "draft": "DRAFT",

    "starred": "STARRED",

    "important": "IMPORTANT",

    "trash": "TRASH",

    "spam": "SPAM",

    "unread": "UNREAD",

    "personal": "CATEGORY_PERSONAL",

    "social": "CATEGORY_SOCIAL",

    "promotions": "CATEGORY_PROMOTIONS",

    "updates": "CATEGORY_UPDATES",

    "forums": "CATEGORY_FORUMS"
}


class GmailLabels:

    def __init__(self):

        self.client = GmailClient()

        self.service = self.client.get_service()

    def list_labels(self):

        response = (
            self.service.users()
            .labels()
            .list(
                userId="me"
            )
            .execute()
        )

        labels = response.get(
            "labels",
            []
        )

        return [
            {
                "id": label.get("id"),
                "name": label.get("name"),
                "type": label.get("type")
            }
            for label in labels
        ]

    def get_label(self, label_id: str):

        if not label_id:

            raise ValueError(
                "label_id is required."
            )

        return (
            self.service.users()
            .labels()
            .get(
                userId="me",
                id=label_id
            )
            .execute()
        )

    def get_system_label(
        self,
        name: str
    ):

        return SYSTEM_LABELS.get(
            name.lower()
        )