"""
Tool permission resolver.

Determines whether an agent may execute
a particular tool action.
"""

from permissions.models import (
    PermissionDecision,
    PermissionResult,
    ToolRequest
)


class PermissionResolver:

    def __init__(
        self,
        permission_manager
    ):

        self.permission_manager = (
            permission_manager
        )

    # ============================================================
    # RESOLVE
    # ============================================================

    def resolve(
        self,
        request: ToolRequest
    ):

        agent_id = (
            request.agent_id
        )

        tool_name = (
            request.tool_name
        )

        rule = (
            self.permission_manager
            .get_rule(
                agent_id,
                tool_name
            )
        )

        # --------------------------------------------------------
        # Unknown action
        # --------------------------------------------------------

        if rule is None:

            return PermissionResult(

                decision=(
                    PermissionDecision.DENY
                ),

                reason=(
                    "No permission rule "
                    "exists for this agent "
                    "and tool."
                ),

                requires_approval=False
            )

        # --------------------------------------------------------
        # Explicit allow
        # --------------------------------------------------------

        if rule == "ALLOW":

            return PermissionResult(

                decision=(
                    PermissionDecision.ALLOW
                ),

                reason=(
                    "Tool action is allowed."
                )
            )

        # --------------------------------------------------------
        # User approval
        # --------------------------------------------------------

        if rule == "ASK_USER":

            return PermissionResult(

                decision=(
                    PermissionDecision.ASK_USER
                ),

                reason=(
                    "This action requires "
                    "user approval."
                ),

                requires_approval=True
            )

        # --------------------------------------------------------
        # Explicit deny
        # --------------------------------------------------------

        if rule == "DENY":

            return PermissionResult(

                decision=(
                    PermissionDecision.DENY
                ),

                reason=(
                    "This action is explicitly "
                    "denied by policy."
                )
            )

        # --------------------------------------------------------
        # Safe default
        # --------------------------------------------------------

        return PermissionResult(

            decision=(
                PermissionDecision.DENY
            ),

            reason=(
                "Unknown permission decision."
            )
        )