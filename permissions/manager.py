"""
Permission rule manager.
"""


class PermissionManager:

    def __init__(
        self,
        rules=None
    ):

        self.rules = (
            rules
            or {}
        )

    # ============================================================
    # SET RULE
    # ============================================================

    def set_rule(
        self,
        agent_id,
        tool_name,
        decision
    ):

        if agent_id not in self.rules:

            self.rules[
                agent_id
            ] = {}

        self.rules[
            agent_id
        ][
            tool_name
        ] = decision

    # ============================================================
    # GET RULE
    # ============================================================

    def get_rule(
        self,
        agent_id,
        tool_name
    ):

        agent_rules = self.rules.get(
            agent_id,
            {}
        )

        return agent_rules.get(
            tool_name
        )

    # ============================================================
    # CHECK RULE
    # ============================================================

    def is_allowed(
        self,
        agent_id,
        tool_name
    ):

        return (
            self.get_rule(
                agent_id,
                tool_name
            )
            == "ALLOW"
        )

    # ============================================================
    # CHECK APPROVAL
    # ============================================================

    def requires_approval(
        self,
        agent_id,
        tool_name
    ):

        return (
            self.get_rule(
                agent_id,
                tool_name
            )
            == "ASK_USER"
        )

    # ============================================================
    # CHECK DENIED
    # ============================================================

    def is_denied(
        self,
        agent_id,
        tool_name
    ):

        return (
            self.get_rule(
                agent_id,
                tool_name
            )
            == "DENY"
        )