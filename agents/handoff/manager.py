"""
Agent handoff manager.
"""

import uuid

from agents.handoff.models import (
    HandoffRequest
)


class HandoffManager:

    def __init__(
        self,
        agent_registry,
        communication_manager
    ):

        self.registry = (
            agent_registry
        )

        self.communication = (
            communication_manager
        )

        self.handoffs = {}

    def create_handoff(
        self,
        task_id: int,
        from_agent: str,
        to_agent: str,
        objective: str,
        context=None,
        reason=""
    ):

        # ------------------------------
        # Verify source agent
        # ------------------------------

        if not self.registry.exists(
            from_agent
        ):

            raise ValueError(
                f"Unknown source agent: "
                f"{from_agent}"
            )

        # ------------------------------
        # Verify destination
        # ------------------------------

        if not self.registry.exists(
            to_agent
        ):

            raise ValueError(
                f"Unknown destination agent: "
                f"{to_agent}"
            )

        target = self.registry.get(
            to_agent
        )

        if target.status != "available":

            raise RuntimeError(
                f"Agent '{to_agent}' "
                f"is not available."
            )

        # ------------------------------
        # Create handoff
        # ------------------------------

        handoff = HandoffRequest(

            handoff_id=str(
                uuid.uuid4()
            ),

            task_id=task_id,

            from_agent=from_agent,

            to_agent=to_agent,

            objective=objective,

            context=context or {},

            reason=reason
        )

        self.handoffs[
            handoff.handoff_id
        ] = handoff

        # ------------------------------
        # Send handoff message
        # ------------------------------

        self.communication.send(

            sender=from_agent,

            receiver=to_agent,

            message_type="handoff",

            content={

                "handoff_id":
                    handoff.handoff_id,

                "task_id":
                    task_id,

                "objective":
                    objective,

                "context":
                    context or {},

                "reason":
                    reason
            },

            correlation_id=(
                handoff.handoff_id
            )
        )

        return handoff

    def accept(
        self,
        handoff_id: str
    ):

        handoff = self.handoffs.get(
            handoff_id
        )

        if not handoff:

            raise KeyError(
                f"Handoff not found: "
                f"{handoff_id}"
            )

        handoff.status = "accepted"

        return handoff

    def complete(
        self,
        handoff_id: str
    ):

        handoff = self.handoffs.get(
            handoff_id
        )

        if not handoff:

            raise KeyError(
                f"Handoff not found: "
                f"{handoff_id}"
            )

        handoff.status = "completed"

        return handoff

    def reject(
        self,
        handoff_id: str,
        reason: str
    ):

        handoff = self.handoffs.get(
            handoff_id
        )

        if not handoff:

            raise KeyError(
                f"Handoff not found: "
                f"{handoff_id}"
            )

        handoff.status = "rejected"

        handoff.context[
            "rejection_reason"
        ] = reason

        return handoff