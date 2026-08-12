class ApprovalManager:

    SENSITIVE_ACTIONS = {
        "trash",
        "send",
        "delete"
    }

    def requires_approval(
        self,
        action: str
    ):

        return action in self.SENSITIVE_ACTIONS