"""
Central AI Policy Engine.

Determines whether an AI action can be executed
automatically, requires user approval, or should
be denied.
"""

from policy.models import PolicyDecision

from policy.rules import (
    is_sensitive_action,
    is_sensitive_category
)
from policy.preferences import (
    UserPreferenceManager
)

class PolicyEngine:

    def __init__(self):

        self.preferences = (
            UserPreferenceManager()
        )

    def evaluate(
        self,
        action: str,
        context: dict | None = None
    ):

        context = context or {}

        user_preferences = (
            self.preferences.load()
        )

        category = context.get(
            "category"
        )

        priority = context.get(
            "priority"
        )

        # -----------------------------------------
        # Blocked actions
        # -----------------------------------------

        blocked_actions = (
            user_preferences
            .get("actions", {})
            .get("blocked", [])
        )

        if action in blocked_actions:

            return PolicyDecision(
                action=action,
                decision="DENY",
                reason=(
                    "Action is blocked "
                    "by user preferences."
                )
            )

        # -----------------------------------------
        # Sensitive categories
        # -----------------------------------------

        sensitive_categories = (
            user_preferences
            .get("email", {})
            .get(
                "always_require_approval",
                []
            )
        )

        if category in sensitive_categories:

            return PolicyDecision(
                action=action,
                decision="APPROVAL_REQUIRED",
                reason=(
                    "This category always "
                    "requires approval."
                ),
                requires_approval=True
            )

        # -----------------------------------------
        # Email auto reply
        # -----------------------------------------

        if action == "send_email":

            email_preferences = (
                user_preferences.get(
                    "email",
                    {}
                )
            )

            auto_reply_enabled = (
                email_preferences.get(
                    "auto_reply_enabled",
                    False
                )
            )

            allowed_categories = (
                email_preferences.get(
                    "auto_reply_categories",
                    []
                )
            )

            max_priority = (
                email_preferences.get(
                    "auto_reply_max_priority",
                    "low"
                )
            )

            priority_levels = {
                "low": 1,
                "medium": 2,
                "high": 3,
                "urgent": 4
            }

            current_priority = (
                priority_levels.get(
                    priority,
                    4
                )
            )

            allowed_priority = (
                priority_levels.get(
                    max_priority,
                    1
                )
            )

            if (
                auto_reply_enabled
                and category in allowed_categories
                and current_priority <= allowed_priority
            ):

                return PolicyDecision(
                    action=action,
                    decision="ALLOW",
                    reason=(
                        "User preferences "
                        "allow this automatic reply."
                    ),
                    requires_approval=False
                )

            return PolicyDecision(
                action=action,
                decision="APPROVAL_REQUIRED",
                reason=(
                    "Automatic sending is "
                    "not allowed for this email."
                ),
                requires_approval=True
            )

        # -----------------------------------------
        # Default
        # -----------------------------------------

        return PolicyDecision(
            action=action,
            decision="ALLOW",
            reason=(
                "Action is allowed."
            ),
            requires_approval=False
        )