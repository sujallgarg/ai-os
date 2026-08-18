"""
Memory access control.
"""


class MemoryPermissionManager:

    def __init__(self):

        self.rules = {}

    # ============================================================
    # ALLOW
    # ============================================================

    def allow(
        self,
        agent_id,
        memory_type
    ):

        self.rules.setdefault(
            agent_id,
            set()
        ).add(
            memory_type
        )

    # ============================================================
    # CHECK
    # ============================================================

    def can_read(
        self,
        agent_id,
        memory
    ):

        # Private memory can only be read
        # by the owning agent.

        if memory.memory_type == "private":

            return (
                memory.agent_id
                == agent_id
            )

        allowed = self.rules.get(
            agent_id,
            set()
        )

        return (
            memory.memory_type
            in allowed
        )