"""
Scheduler state management.
"""

import json
from pathlib import Path


class SchedulerState:

    def __init__(
        self,
        file_path="data/scheduler_state.json"
    ):

        self.file_path = Path(
            file_path
        )

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def load(self):

        if not self.file_path.exists():

            return {
                "processed_messages": []
            }

        try:

            return json.loads(
                self.file_path.read_text()
            )

        except Exception:

            return {
                "processed_messages": []
            }

    def is_processed(
        self,
        message_id: str
    ):

        state = self.load()

        return message_id in state.get(
            "processed_messages",
            []
        )

    def mark_processed(
        self,
        message_id: str
    ):

        state = self.load()

        processed = state.setdefault(
            "processed_messages",
            []
        )

        if message_id not in processed:

            processed.append(
                message_id
            )

        # Keep only the most recent 500 IDs.
        state["processed_messages"] = (
            processed[-500:]
        )

        self.file_path.write_text(
            json.dumps(
                state,
                indent=2
            )
        )

    def clear(self):

        state = {
            "processed_messages": []
        }

        self.file_path.write_text(
            json.dumps(
                state,
                indent=2
            )
        )