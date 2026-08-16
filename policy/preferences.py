"""
User preference management.

Stores the rules that determine how autonomous
the AI is allowed to be.
"""

import json
from pathlib import Path


class UserPreferenceManager:

    def __init__(
        self,
        file_path="data/user_preferences.json"
    ):

        self.file_path = Path(
            file_path
        )

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def default_preferences(self):

        return {
            "email": {
                "auto_reply_enabled": False,

                "auto_reply_categories": [
                    "client"
                ],

                "auto_reply_max_priority": "low",

                "always_require_approval": [
                    "finance",
                    "legal"
                ],

                "blocked_categories": [
                    "spam"
                ]
            },

            "actions": {
                "blocked": [],

                "approval_required": [
                    "send_email",
                    "delete_file",
                    "make_payment",
                    "place_trade",
                    "purchase"
                ]
            }
        }

    def load(self):

        if not self.file_path.exists():

            preferences = (
                self.default_preferences()
            )

            self.save(
                preferences
            )

            return preferences

        try:

            return json.loads(
                self.file_path.read_text()
            )

        except Exception:

            preferences = (
                self.default_preferences()
            )

            self.save(
                preferences
            )

            return preferences

    def save(
        self,
        preferences: dict
    ):

        self.file_path.write_text(
            json.dumps(
                preferences,
                indent=2
            )
        )

    def update(
        self,
        preferences: dict
    ):

        self.save(
            preferences
        )

    def get(
        self,
        key: str,
        default=None
    ):

        preferences = self.load()

        return preferences.get(
            key,
            default
        )