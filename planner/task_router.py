class TaskRouter:
    def route(self, task):
        if isinstance(task, dict):
            text = task.get("intent") or task.get("task") or ""
        else:
            text = str(task)

        if "gmail" in text.lower():
            return "email"
        return "general"