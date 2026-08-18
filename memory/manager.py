"""
Shared Agent Memory Manager.
"""

from datetime import datetime

from memory.models import Memory

from memory.store import MemoryStore

from memory.permissions import (
    MemoryPermissionManager
)


class MemoryManager:

    def __init__(
        self,
        store=None,
        permissions=None
    ):

        self.store = (

            store
            or MemoryStore()
        )

        self.permissions = (

            permissions
            or MemoryPermissionManager()
        )

    # ============================================================
    # WRITE MEMORY
    # ============================================================

    def remember(
        self,
        key,
        value,
        agent_id,
        memory_type="shared",
        importance=5,
        metadata=None
    ):

        memory = Memory(

            key=key,

            value=value,

            agent_id=agent_id,

            memory_type=memory_type,

            importance=importance,

            metadata=(
                metadata
                or {}
            )
        )

        self.store.save(
            memory
        )

        return memory

    # ============================================================
    # READ MEMORY
    # ============================================================

    def recall(
        self,
        key,
        agent_id
    ):

        memory = self.store.get(
            key
        )

        if memory is None:

            return None

        # --------------------------------------------------------
        # Expiration
        # --------------------------------------------------------

        if (
            memory.expires_at
            and memory.expires_at
            < datetime.utcnow()
        ):

            self.store.delete(
                key
            )

            return None

        # --------------------------------------------------------
        # Permission
        # --------------------------------------------------------

        if not self.permissions.can_read(

            agent_id,

            memory
        ):

            raise PermissionError(

                f"Agent '{agent_id}' "
                f"cannot read memory "
                f"'{key}'."
            )

        return memory

    # ============================================================
    # SEARCH
    # ============================================================

    def search(
        self,
        agent_id,
        memory_type=None
    ):

        memories = []

        for memory in self.store.all():

            # --------------------------------
            # Type filter
            # --------------------------------

            if (
                memory_type
                and memory.memory_type
                != memory_type
            ):

                continue

            # --------------------------------
            # Permission
            # --------------------------------

            if not self.permissions.can_read(

                agent_id,

                memory
            ):

                continue

            memories.append(
                memory
            )

        # Highest importance first.

        memories.sort(

            key=lambda memory:
                memory.importance,

            reverse=True
        )

        return memories

    # ============================================================
    # FORGET
    # ============================================================

    def forget(
        self,
        key,
        agent_id
    ):

        memory = self.store.get(
            key
        )

        if memory is None:

            return False

        if (
            memory.agent_id
            != agent_id
        ):

            raise PermissionError(

                "Only the owning agent "
                "can delete this memory."
            )

        self.store.delete(
            key
        )

        return True