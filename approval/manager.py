import uuid

from approval.models import (
    ApprovalRequest,
    ApprovalStatus
)

from approval.store import (
    ApprovalStore
)


class ApprovalManager:

    def __init__(
        self,
        store=None
    ):

        self.store = (
            store
            or ApprovalStore()
        )

    def create_request(
        self,
        agent_id,
        tool_name,
        action,
        parameters=None,
        reason=""
    ):

        request = ApprovalRequest(

            id=str(
                uuid.uuid4()
            ),

            agent_id=agent_id,

            tool_name=tool_name,

            action=action,

            parameters=(
                parameters
                or {}
            ),

            reason=reason
        )

        self.store.save(
            request
        )

        return request

    def approve(
        self,
        request_id
    ):

        request = self.store.get(
            request_id
        )

        if not request:
            raise ValueError(
                "Approval request not found."
            )

        request.status = (
            ApprovalStatus.APPROVED
        )

        return request

    def reject(
        self,
        request_id
    ):

        request = self.store.get(
            request_id
        )

        if not request:
            raise ValueError(
                "Approval request not found."
            )

        request.status = (
            ApprovalStatus.REJECTED
        )

        return request