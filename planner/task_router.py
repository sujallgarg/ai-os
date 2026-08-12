class TaskRouter:
    def route(self, task):
        if isinstance(task, dict):
            text = f"{task.get('intent', '')} {task.get('task', '')} {task.get('tool', '')} {task.get('agent', '')}"
            if not text.strip():
                text = str(task)
        else:
            text = str(task)

        text_lower = text.lower()
        if any(keyword in text_lower for keyword in ["gmail", "email", "mail", "inbox"]):
            return "email"
        return "general"