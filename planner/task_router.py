class TaskRouter:

    def route(self, task):

        text = task.get(
            "task",
            ""
        ).lower()

        if any(
            word in text
            for word in [
                "gmail",
                "email",
                "emails",
                "mail"
            ]
        ):

            return "email"

        return "general"