"""
High-level handoff service.
"""

from agents.handoff.manager import (
    HandoffManager
)


class AgentHandoffService:

    def __init__(
        self,
        agent_registry,
        communication_manager
    ):

        self.manager = HandoffManager(

            agent_registry,

            communication_manager
        )

    def handoff(
        self,
        task_id: int,
        from_agent: str,
        to_agent: str,
        objective: str,
        context=None,
        reason=""
    ):

        return self.manager.create_handoff(

            task_id=task_id,

            from_agent=from_agent,

            to_agent=to_agent,

            objective=objective,

            context=context,

            reason=reason
        )

    def accept(
        self,
        handoff_id
    ):

        return self.manager.accept(
            handoff_id
        )

    def complete(
        self,
        handoff_id
    ):

        return self.manager.complete(
            handoff_id
        )

    def reject(
        self,
        handoff_id,
        reason
    ):

        return self.manager.reject(

            handoff_id,

            reason
        )