"""
SQLite memory storage.
"""

import sqlite3
from pathlib import Path


class MemoryStore:

    def __init__(
        self,
        database_path="data/memory.db"
    ):

        path = Path(
            database_path
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            str(path),
            check_same_thread=False
        )

        self._create_table()

    def _create_table(self):

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (

                id TEXT PRIMARY KEY,

                user_id TEXT NOT NULL,

                memory_type TEXT NOT NULL,

                key TEXT NOT NULL,

                value TEXT NOT NULL,

                importance REAL DEFAULT 0.5,

                source TEXT DEFAULT 'user',

                created_at TEXT NOT NULL,

                updated_at TEXT NOT NULL
            )
            """
        )

        self.connection.commit()

    def save(
        self,
        memory
    ):

        self.connection.execute(
            """
            INSERT OR REPLACE INTO memories
            (
                id,
                user_id,
                memory_type,
                key,
                value,
                importance,
                source,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                memory.id,
                memory.user_id,
                memory.memory_type,
                memory.key,
                memory.value,
                memory.importance,
                memory.source,
                memory.created_at,
                memory.updated_at
            )
        )

        self.connection.commit()

    def get(
        self,
        memory_id
    ):

        cursor = self.connection.execute(
            """
            SELECT
                id,
                user_id,
                memory_type,
                key,
                value,
                importance,
                source,
                created_at,
                updated_at
            FROM memories
            WHERE id = ?
            """,
            (memory_id,)
        )

        return cursor.fetchone()

    def get_by_user(
        self,
        user_id
    ):

        cursor = self.connection.execute(
            """
            SELECT
                id,
                user_id,
                memory_type,
                key,
                value,
                importance,
                source,
                created_at,
                updated_at
            FROM memories
            WHERE user_id = ?
            ORDER BY importance DESC
            """,
            (user_id,)
        )

        return cursor.fetchall()

    def delete(
        self,
        memory_id
    ):

        self.connection.execute(
            """
            DELETE FROM memories
            WHERE id = ?
            """,
            (memory_id,)
        )

        self.connection.commit()