"""
Application dependency container.

All major AI services are created here so
API routes can access the same instances.
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


application = Application()