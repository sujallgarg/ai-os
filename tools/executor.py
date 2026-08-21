from executor.result import (
    ExecutionResult
)

from permissions.models import (
    ToolRequest,
    PermissionDecision
)


class ToolExecutor:

    def __init__(
        self,
        tool_registry,
        permission_resolver,
        approval_manager
    ):

        self.tool_registry = (
            tool_registry
        )

        self.permission_resolver = (
            permission_resolver
        )

        self.approval_manager = (
            approval_manager
        )

    async def execute(
        self,
        tool_name,
        parameters,
        agent_id,
        task_id,
        job_id=None,
        context=None
    ):

        # ========================================================
        # BUILD REQUEST
        # ========================================================

        request = ToolRequest(

            agent_id=agent_id,

            tool_name=tool_name,

            action=tool_name,

            parameters=parameters
        )

        # ========================================================
        # PERMISSION
        # ========================================================

        permission = (
            self.permission_resolver.resolve(
                request
            )
        )

        # ========================================================
        # DENIED
        # ========================================================

        if (
            permission.decision
            == PermissionDecision.DENY
        ):

            return ExecutionResult(

                task_id=task_id,

                status="failed",

                error=(
                    "Tool execution denied: "
                    + permission.reason
                )
            )

        # ========================================================
        # APPROVAL REQUIRED
        # ========================================================

        if (
            permission.decision
            == PermissionDecision.ASK_USER
        ):

            approval = (
                self.approval_manager
                .create_request(

                    agent_id=agent_id,

                    tool_name=tool_name,

                    action=tool_name,

                    parameters=parameters,

                    reason=(
                        permission.reason
                    )
                )
            )

            return ExecutionResult(

                task_id=task_id,

                status="waiting_approval",

                approval_id=approval.id,

                metadata={

                    "job_id": job_id,

                    "tool_name": tool_name
                }
            )

        # ========================================================
        # ALLOWED
        # ========================================================

        tool = (
            self.tool_registry
            .get(tool_name)
        )

        if tool is None:

            return ExecutionResult(

                task_id=task_id,

                status="failed",

                error=(
                    f"Unknown tool: {tool_name}"
                )
            )

        try:

            result = await tool.execute(
                parameters
            )

            return ExecutionResult(

                task_id=task_id,

                status="completed",

                output=result,

                metadata={

                    "tool_name":
                        tool_name
                }
            )

        except Exception as error:

            return ExecutionResult(

                task_id=task_id,

                status="failed",

                error=str(error)
            )