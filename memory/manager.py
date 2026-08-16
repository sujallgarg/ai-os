"""
Memory Manager.

Provides a simple interface for storing,
retrieving and deleting user memories.
"""

import uuid
from datetime import datetime

from memory.models import Memory
from memory.store import MemoryStore


class MemoryManager:

    def __init__(self):

        self.store = MemoryStore()

    def remember(
        self,
        user_id: str,
        memory_type: str,
        key: str,
        value: str,
        importance: float = 0.5,
        source: str = "user"
    ):

        now = datetime.utcnow().isoformat()

        memory = Memory(

            id=str(
                uuid.uuid4()
            ),

            user_id=user_id,

            memory_type=memory_type,

            key=key,

            value=value,

            importance=importance,

            created_at=now,

            updated_at=now,

            source=source
        )

        self.store.save(
            memory
        )

        return memory

    def get_user_memories(
        self,
        user_id: str
    ):

        return self.store.get_by_user(
            user_id
        )

    def forget(
        self,
        memory_id: str
    ):

        self.store.delete(
            memory_id
        )