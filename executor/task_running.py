import inspect
from executor.result import ExecutionResult


class TaskRunner:

    def __init__(
        self,
        agent_manager,
        capability_matcher=None,
        tool_executor=None
    ):
        self.agent_manager = agent_manager
        self.capability_matcher = capability_matcher
        self.tool_executor = tool_executor

    async def run(
        self,
        task,
        context=None
    ):
        print(f"[TaskRunner] Starting task {task.id}")
        context = context or {}

        try:
            # ====================================================
            # FIND AGENT
            # ====================================================
            agent = None
            task_agent_name = getattr(task, "agent", None)

            if task_agent_name and hasattr(self.agent_manager, "get"):
                agent = self.agent_manager.get(task_agent_name)

            # ====================================================
            # CAPABILITY MATCHING
            # ====================================================
            if agent is None and self.capability_matcher:
                req_caps = getattr(task, "required_capabilities", [])
                agent = self.capability_matcher.match(req_caps)

            if agent is None and task_agent_name:
                agent = task_agent_name

            if agent is None:
                return ExecutionResult(
                    task_id=task.id,
                    status="failed",
                    error="No suitable agent was found."
                )

            agent_name = getattr(agent, "name", str(agent))

            # ====================================================
            # TOOL EXECUTION
            # ====================================================
            tool_name = getattr(task, "tool_name", None)
            if tool_name and self.tool_executor:
                result = await self.tool_executor.execute(
                    tool_name=tool_name,
                    parameters=getattr(task, "parameters", {}),
                    agent_id=agent_name,
                    task_id=task.id,
                    job_id=context.get("job_id"),
                    context=context
                )

                if isinstance(result, ExecutionResult):
                    return result

                return ExecutionResult(
                    task_id=task.id,
                    status="completed",
                    output=result,
                    metadata={"agent": agent_name, "tool": tool_name}
                )

            # ====================================================
            # AGENT-ONLY TASK
            # ====================================================
            if hasattr(agent, "execute"):
                res = agent.execute(task=task, context=context)
                if inspect.isawaitable(res):
                    res = await res

                if isinstance(res, ExecutionResult):
                    return res

                return ExecutionResult(
                    task_id=task.id,
                    status="completed",
                    output=res,
                    metadata={"agent": agent_name}
                )

            if hasattr(self.agent_manager, "execute"):
                res = self.agent_manager.execute(
                    agent_name=agent_name,
                    task={
                        "id": task.id,
                        "action": getattr(task, "action", ""),
                        "parameters": getattr(task, "parameters", {}),
                        "description": getattr(task, "description", "")
                    }
                )
                if inspect.isawaitable(res):
                    res = await res

                if isinstance(res, ExecutionResult):
                    return res

                return ExecutionResult(
                    task_id=task.id,
                    status="completed",
                    output=res,
                    metadata={"agent": agent_name}
                )

            return ExecutionResult(
                task_id=task.id,
                status="failed",
                error="Agent cannot execute this task."
            )

        except Exception as error:
            return ExecutionResult(
                task_id=task.id,
                status="failed",
                error=str(error)
            )