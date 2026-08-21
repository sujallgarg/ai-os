"""
executor/executor.py

Main execution engine for the autonomous AI platform.

Responsibilities:
    1. Receive a task graph / task list.
    2. Resolve task dependencies.
    3. Identify tasks that are ready to execute.
    4. Execute independent tasks concurrently.
    5. Route tasks to appropriate agents.
    6. Route tool calls through the ToolExecutor.
    7. Collect execution results.
    8. Detect blocked/deadlocked tasks.
    9. Report progress.
    10. Return a complete execution result.

Important:

The Executor does NOT bypass the permission system.

The intended flow is:

    Task
      ↓
    Executor
      ↓
    TaskRunner
      ↓
    ToolExecutor
      ↓
    PermissionResolver
      ↓
    ALLOW / ASK_USER / DENY
"""

from __future__ import annotations

import asyncio
import inspect
import logging
from typing import Any, Callable, Iterable

from executor.result import ExecutionResult
from executor.task_running import TaskRunner
from events.models import (
    SystemEvent
)

from events.manager import (
    event_manager
)


logger = logging.getLogger(__name__)


class Executor:
    """
    Main task execution engine.

    The executor works with a DAG-like task structure where each
    task can depend on one or more previous tasks.
    """

    def __init__(
        self,
        agent_manager=None,
        log_service=None,
        recovery_manager=None,
        retry_manager=None,
        timeout_manager=None,
        supervisor=None,
        capability_matcher=None,
        memory_manager=None,
        permission_resolver=None,
        tool_executor=None,
        approval_manager=None,
        job_manager=None,
        progress_callback: Callable[
            [dict[str, Any]], Any
        ] | None = None,
        max_parallel_tasks: int = 5,
    ):
        self.agent_manager = agent_manager

        self.log_service = log_service

        self.recovery_manager = (
            recovery_manager
        )

        self.retry_manager = retry_manager

        self.timeout_manager = (
            timeout_manager
        )

        self.supervisor = supervisor

        self.capability_matcher = (
            capability_matcher
        )

        self.memory_manager = (
            memory_manager
        )

        self.permission_resolver = (
            permission_resolver
        )

        self.tool_executor = (
            tool_executor
        )

        self.approval_manager = (
            approval_manager
        )

        self.job_manager = (
            job_manager
        )

        self.progress_callback = (
            progress_callback
        )

        self.max_parallel_tasks = max(
            1,
            max_parallel_tasks
        )

        self.task_runner = TaskRunner(
            agent_manager=(
                self.agent_manager
            ),
            capability_matcher=(
                self.capability_matcher
            ),
            tool_executor=(
                self.tool_executor
            ),
        )

    # ============================================================
    # PUBLIC API
    # ============================================================

    async def execute_task_graph(
        self,
        tasks: Iterable[Any],
        context: dict[str, Any] | None = None,
        job_id: str | None = None,
        goal: str | None = None,
    ) -> dict[int, ExecutionResult]:
        """
        Execute a complete task graph.

        Tasks are executed only when all dependencies have
        completed successfully.

        Independent tasks may run concurrently.
        """

        context = dict(
            context or {}
        )

        if job_id is not None:
            context["job_id"] = job_id

        if goal is not None:
            context["goal"] = goal

        task_list = list(tasks)

        if not task_list:
            return {}

        pending: dict[int, Any] = {
            self._task_id(task): task
            for task in task_list
        }

        results: dict[
            int,
            ExecutionResult
        ] = {}

        total_tasks = len(
            pending
        )

        completed_count = 0

        logger.info(
            "Starting task graph with %s tasks",
            total_tasks,
        )

        await self._report_progress(
            job_id=job_id,
            progress=0,
            event="execution.started",
            metadata={
                "total_tasks": total_tasks
            },
        )

        while pending:

            ready_tasks = (
                self._get_ready_tasks(
                    pending=list(
                        pending.values()
                    ),
                    results=results,
                )
            )

            # ----------------------------------------------------
            # DEADLOCK / BLOCKED TASK DETECTION
            # ----------------------------------------------------

            if not ready_tasks:

                logger.error(
                    "No executable tasks remain, "
                    "but %s pending tasks exist.",
                    len(pending),
                )

                for task in pending.values():

                    task_id = (
                        self._task_id(task)
                    )

                    results[task_id] = (
                        ExecutionResult(
                            task_id=task_id,
                            status="blocked",
                            error=(
                                "Task dependencies "
                                "cannot be satisfied."
                            ),
                            metadata={
                                "reason": (
                                    "dependency_deadlock"
                                )
                            },
                        )
                    )

                await self._report_progress(
                    job_id=job_id,
                    progress=self._calculate_progress(
                        completed_count,
                        total_tasks,
                    ),
                    event="execution.blocked",
                    metadata={
                        "remaining_tasks": len(
                            pending
                        )
                    },
                )

                break

            # ----------------------------------------------------
            # LIMIT CONCURRENT TASKS
            # ----------------------------------------------------

            current_batch = (
                ready_tasks[
                    : self.max_parallel_tasks
                ]
            )

            for task in current_batch:
                task_id = self._task_id(task)
                await self._report_progress(
                    job_id=job_id,
                    progress=self._calculate_progress(
                        completed_count,
                        total_tasks,
                    ),
                    event="task.started",
                    metadata={
                        "task_id": task_id,
                        "description": getattr(task, "description", ""),
                    },
                )

            logger.info(
                "Executing %s ready tasks",
                len(current_batch),
            )

            # ----------------------------------------------------
            # EXECUTE READY TASKS CONCURRENTLY
            # ----------------------------------------------------

            batch_results = await asyncio.gather(

                *[
                    self._execute_single_task(
                        task=task,
                        context=context,
                    )
                    for task in current_batch
                ],

                return_exceptions=False,
            )

            # ----------------------------------------------------
            # STORE RESULTS
            # ----------------------------------------------------

            for task, result in zip(
                current_batch,
                batch_results,
            ):

                task_id = (
                    self._task_id(task)
                )

                results[task_id] = result

                pending.pop(
                    task_id,
                    None,
                )

                if result.status == "completed":

                    completed_count += 1

            # ----------------------------------------------------
            # UPDATE PROGRESS
            # ----------------------------------------------------

            progress = (
                self._calculate_progress(
                    completed_count,
                    total_tasks,
                )
            )

            await self._report_progress(
                job_id=job_id,
                progress=progress,
                event="execution.progress",
                metadata={
                    "completed_tasks":
                        completed_count,

                    "total_tasks":
                        total_tasks,

                    "remaining_tasks":
                        len(pending),
                },
            )

            # ----------------------------------------------------
            # STOP IF A TASK REQUIRES APPROVAL
            # ----------------------------------------------------

            waiting_for_approval = any(

                result.status
                == "waiting_approval"

                for result
                in batch_results
            )

            if waiting_for_approval:

                logger.info(
                    "Execution paused because "
                    "approval is required."
                )

                await self._report_progress(
                    job_id=job_id,
                    progress=progress,
                    event="execution.waiting_approval",
                    metadata={},
                )

                break

            # ----------------------------------------------------
            # FAILURE HANDLING
            # ----------------------------------------------------

            permanent_failure = any(

                result.status == "failed"

                for result
                in batch_results
            )

            if permanent_failure:

                logger.warning(
                    "One or more tasks failed."
                )

                # Do not automatically abort every
                # independent task here.
                #
                # Dependent tasks will remain blocked
                # because their dependency did not complete.

        # --------------------------------------------------------
        # FINAL STATUS
        # --------------------------------------------------------

        await self._report_progress(
            job_id=job_id,
            progress=self._calculate_progress(
                completed_count,
                total_tasks,
            ),
            event="execution.finished",
            metadata={
                "completed_tasks":
                    completed_count,

                "total_tasks":
                    total_tasks,

                "remaining_tasks":
                    len(pending),
            },
        )

        logger.info(
            "Task graph execution finished."
        )

        return results

    # ============================================================
    # SINGLE TASK
    # ============================================================

    async def _execute_single_task(
        self,
        task: Any,
        context: dict[str, Any],
    ) -> ExecutionResult:
        """
        Execute one task through TaskRunner.

        This method is intentionally small because TaskRunner
        owns the actual agent/tool execution.
        """

        task_id = (
            self._task_id(task)
        )

        logger.info(
            "Starting task %s",
            task_id,
        )

        await self._report_progress(
            job_id=context.get(
                "job_id"
            ),
            progress=None,
            event="task.started",
            metadata={
                "task_id": task_id,

                "description":
                    getattr(
                        task,
                        "description",
                        "",
                    ),

                "agent":
                    getattr(
                        task,
                        "agent",
                        None,
                    ),

                "tool":
                    getattr(
                        task,
                        "tool_name",
                        None,
                    ),
            },
        )

        try:

            result = await self.task_runner.run(
                task=task,
                context=context,
            )

            if not isinstance(
                result,
                ExecutionResult,
            ):

                result = ExecutionResult(

                    task_id=task_id,

                    status="completed",

                    output=result,
                )

            await self._report_progress(
                job_id=context.get(
                    "job_id"
                ),
                progress=None,
                event=(
                    "task."
                    f"{result.status}"
                ),
                metadata={
                    "task_id": task_id,
                    "error": result.error,
                },
            )

            return result

        except asyncio.CancelledError:

            logger.warning(
                "Task %s was cancelled.",
                task_id,
            )

            return ExecutionResult(

                task_id=task_id,

                status="cancelled",

                error="Task was cancelled.",
            )

        except Exception as error:

            logger.exception(
                "Task %s failed.",
                task_id,
            )

            recovered = await (
                self._attempt_recovery(
                    task,
                    error,
                    context,
                )
            )

            if recovered is not None:

                return recovered

            return ExecutionResult(

                task_id=task_id,

                status="failed",

                error=str(error),
            )

    # ============================================================
    # DEPENDENCY RESOLUTION
    # ============================================================

    def _dependencies_completed(
        self,
        task: Any,
        results: dict[
            int,
            ExecutionResult
        ],
    ) -> bool:
        """
        Return True only if every dependency has completed.

        A dependency that is:
            failed
            blocked
            waiting_approval
            cancelled

        is NOT considered completed.
        """

        dependencies = getattr(
            task,
            "depends_on",
            None,
        )

        if dependencies is None:

            # Support older task models that may use
            # "dependencies".

            dependencies = getattr(
                task,
                "dependencies",
                [],
            )

        for dependency_id in (
            dependencies or []
        ):

            dependency_result = (
                results.get(
                    dependency_id
                )
            )

            if dependency_result is None:

                return False

            if (
                dependency_result.status
                != "completed"
            ):

                return False

        return True

    # ============================================================
    # READY TASKS
    # ============================================================

    def _get_ready_tasks(
        self,
        pending: Iterable[Any],
        results: dict[
            int,
            ExecutionResult
        ],
    ) -> list[Any]:
        """
        Return tasks whose dependencies are complete.
        """

        ready_tasks = [

            task

            for task in pending

            if self._dependencies_completed(
                task,
                results,
            )
        ]

        return ready_tasks

    # ============================================================
    # TASK ID
    # ============================================================

    @staticmethod
    def _task_id(
        task: Any
    ) -> int:
        """
        Extract a stable task ID.
        """

        task_id = getattr(
            task,
            "id",
            None,
        )

        if task_id is None:

            raise ValueError(
                "Every task must have an id."
            )

        return int(
            task_id
        )

    # ============================================================
    # PROGRESS
    # ============================================================

    @staticmethod
    def _calculate_progress(
        completed: int,
        total: int,
    ) -> float:
        """
        Calculate percentage progress.
        """

        if total <= 0:

            return 100.0

        return round(
            (
                completed
                / total
            )
            * 100,
            2,
        )

    # ============================================================
    # PROGRESS EVENT
    # ============================================================

    async def _report_progress(
        self,
        job_id: str | None,
        progress: float | None,
        event: str,
        metadata: dict[str, Any],
    ) -> None:
        """
        Report execution events.

        Supports:
            - JobManager
            - custom callback
            - future WebSocket/SSE event system
        """

        payload = {

            "event": event,

            "job_id": job_id,

            "progress": progress,

            "metadata": metadata,
        }

        # --------------------------------------------------------
        # JOB MANAGER
        # --------------------------------------------------------

        if (
            self.job_manager
            and job_id
            and progress is not None
        ):

            try:

                self.job_manager.update_progress(
                    job_id,
                    progress,
                )

            except Exception:

                logger.exception(
                    "Failed to update job progress."
                )

        # --------------------------------------------------------
        # CUSTOM EVENT CALLBACK
        # --------------------------------------------------------

        if self.progress_callback:

            try:

                callback_result = (
                    self.progress_callback(
                        payload
                    )
                )

                if inspect.isawaitable(
                    callback_result
                ):

                    await callback_result

            except Exception:

                logger.exception(
                    "Progress callback failed."
                )

    # ============================================================
    # RECOVERY
    # ============================================================

    async def _attempt_recovery(
        self,
        task: Any,
        error: Exception,
        context: dict[str, Any],
    ) -> ExecutionResult | None:
        """
        Give the configured recovery system an opportunity
        to recover from an execution failure.

        Returns:
            ExecutionResult if recovery succeeded.
            None if no recovery was possible.
        """

        if self.recovery_manager is None:

            return None

        try:

            recovery_method = getattr(
                self.recovery_manager,
                "recover",
                None,
            )

            if recovery_method is None:

                return None

            result = recovery_method(

                task=task,

                error=error,

                context=context,
            )

            if inspect.isawaitable(
                result
            ):

                result = await result

            if result is None:

                return None

            if isinstance(
                result,
                ExecutionResult,
            ):

                return result

            return ExecutionResult(

                task_id=self._task_id(
                    task
                ),

                status="completed",

                output=result,

                metadata={
                    "recovered": True
                },
            )

        except Exception:

            logger.exception(
                "Recovery attempt failed."
            )

            return None

    # ============================================================
    # SYNCHRONOUS COMPATIBILITY WRAPPER
    # ============================================================

    def execute_sync(
        self,
        tasks: Iterable[Any],
        context: dict[str, Any] | None = None,
        job_id: str | None = None,
        goal: str | None = None,
    ) -> dict[int, ExecutionResult]:
        """
        Synchronous wrapper for environments that are not
        already running an asyncio event loop.
        """

        return asyncio.run(
            self.execute_task_graph(
                tasks=tasks,
                context=context,
                job_id=job_id,
                goal=goal,
            )
        )
async def _report_progress(
    self,
    job_id,
    progress,
    event,
    metadata
):

    payload = {
        "event": event,
        "job_id": job_id,
        "progress": progress,
        "metadata": metadata,
    }

    # Existing JobManager update
    if (
        self.job_manager
        and job_id
        and progress is not None
    ):

        self.job_manager.update_progress(
            job_id,
            progress
        )

    # ------------------------------------------------------------
    # REAL-TIME EVENT
    # ------------------------------------------------------------

    user_id = (
        metadata.get(
            "user_id"
        )
        if metadata
        else None
    )

    if user_id:

        await event_manager.publish(

            SystemEvent(

                event=event,

                job_id=job_id,

                task_id=metadata.get(
                    "task_id"
                ),

                agent_id=metadata.get(
                    "agent_id"
                ),

                data=metadata
            ),

            user_id=user_id
        )

    # Existing callback
    if self.progress_callback:

        result = self.progress_callback(
            payload
        )

        if inspect.isawaitable(
            result
        ):

            await result

TaskExecutor = Executor