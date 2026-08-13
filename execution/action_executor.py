"""
Executes actions that have already passed
the approval stage.
"""

from tools.gmail.send import GmailSender


class ActionExecutor:

    def __init__(self):

        self.gmail_sender = GmailSender()

    def execute(
        self,
        request: dict
    ):

        if request.get("status") != "approved":

            raise PermissionError(
                "Action has not been approved."
            )

        action = request.get(
            "action"
        )

        data = request.get(
            "data",
            {}
        )

        if action == "send_email":

            return self.gmail_sender.send_email(
            to=data.get("to"),
            subject=data.get("subject"),
            body=data.get("body"),
            thread_id=data.get(
                "thread_id"
        ),
        in_reply_to=data.get(
            "in_reply_to"
        ),
        references=data.get(
            "references"
        )
    )