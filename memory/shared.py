"""
Shared memory interface for agents.
"""


class SharedMemory:

    def __init__(
        self,
        manager,
        agent_id
    ):

        self.manager = manager

        self.agent_id = agent_id

    # ============================================================
    # REMEMBER
    # ============================================================

    def remember(
        self,
        key,
        value,
        memory_type="shared",
        importance=5,
        metadata=None
    ):

        return self.manager.remember(

            key=key,

            value=value,

            agent_id=self.agent_id,

            memory_type=memory_type,

            importance=importance,

            metadata=metadata
        )

    # ============================================================
    # RECALL
    # ============================================================

    def recall(
        self,
        key
    ):

        return self.manager.recall(

            key=key,

            agent_id=self.agent_id
        )

    # ============================================================
    # SEARCH
    # ============================================================

    def search(
        self,
        memory_type=None
    ):

        return self.manager.search(

            agent_id=self.agent_id,

            memory_type=memory_type
        )

    # ============================================================
    # FORGET
    # ============================================================

    def forget(
        self,
        key
    ):

        return self.manager.forget(

            key=key,

            agent_id=self.agent_id
        )