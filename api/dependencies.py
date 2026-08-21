"""
Application dependency container.

All major AI services are created here so
API routes and background workers can access the same instances.
"""

from memory.manager import MemoryManager
from memory.setup import (
    create_default_permissions
)

from agents.capabilities.registry import (
    CapabilityRegistry
)

from agents.capabilities.matcher import (
    CapabilityMatcher
)

from agents.capabilities.defaults import (
    register_default_agents
)

from permissions.setup import (
    create_permission_system
)

from approval.manager import (
    ApprovalManager
)

from jobs.manager import (
    JobManager
)

from agents.setup import (
    create_agent_manager
)

from planner.multi_agent import (
    MultiAgentPlanner
)

from recovery.manager import (
    RecoveryManager
)

from retry.manager import (
    RetryManager
)

from timeout.manager import (
    TimeoutManager
)

from executor.executor import (
    TaskExecutor
)


class Application:

    def __init__(self):

        # ========================================================
        # MEMORY
        # ========================================================

        memory_permissions = (
            create_default_permissions()
        )

        self.memory_manager = (
            MemoryManager(
                permissions=memory_permissions
            )
        )

        # ========================================================
        # AGENT CAPABILITIES
        # ========================================================

        self.agent_registry = (
            CapabilityRegistry()
        )

        register_default_agents(
            self.agent_registry
        )

        self.capability_matcher = (
            CapabilityMatcher(
                self.agent_registry
            )
        )

        # ========================================================
        # PERMISSIONS
        # ========================================================

        (
            self.permission_manager,
            self.permission_resolver
        ) = create_permission_system()

        # ========================================================
        # APPROVALS
        # ========================================================

        self.approval_manager = (
            ApprovalManager()
        )

        # ========================================================
        # JOBS
        # ========================================================

        self.job_manager = (
            JobManager()
        )

        # ========================================================
        # AGENTS & PLANNER
        # ========================================================

        self.agent_manager = (
            create_agent_manager()
        )

        self.planner = (
            MultiAgentPlanner(
                agent_registry=self.agent_registry
            )
        )

        # ========================================================
        # RESILIENCE (RECOVERY, RETRY, TIMEOUT)
        # ========================================================

        self.recovery_manager = (
            RecoveryManager(
                planner=self.planner
            )
        )

        self.retry_manager = (
            RetryManager()
        )

        self.timeout_manager = (
            TimeoutManager()
        )

        # ========================================================
        # CENTRAL EXECUTOR
        # ========================================================

        self.executor = TaskExecutor(
            agent_manager=self.agent_manager,
            recovery_manager=self.recovery_manager,
            retry_manager=self.retry_manager,
            timeout_manager=self.timeout_manager,
            capability_matcher=self.capability_matcher,
            memory_manager=self.memory_manager,
            permission_resolver=self.permission_resolver
        )


application = Application()