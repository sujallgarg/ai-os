"""
Approval Manager

Controls sensitive actions that require user confirmation
before the AI is allowed to execute them.
"""


class ApprovalManager:

    SENSITIVE_ACTIONS = {
        "send_email",
        "trash_email",
        "delete_email",
        "delete_file",
        "make_payment",
        "place_trade",
        "purchase"
    }

    def requires_approval(
        self,
        action: str
    ):

        return action in self.SENSITIVE_ACTIONS

    def create_request(
        self,
        action: str,
        description: str,
        data: dict | None = None
    ):

        return {
            "status": "pending_approval",
            "action": action,
            "description": description,
            "data": data or {}
        }

    def approve(
        self,
        request: dict
    ):

        if request.get("status") != "pending_approval":

            raise ValueError(
                "This request is not waiting for approval."
            )

        request["status"] = "approved"

        return request

    def reject(
        self,
        request: dict
    ):

        if request.get("status") != "pending_approval":

            raise ValueError(
                "This request is not waiting for approval."
            )

        request["status"] = "rejected"

        return request