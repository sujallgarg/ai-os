"""
Low-level memory storage.

Development implementation:
in-memory dictionary.

Production implementation:
PostgreSQL + Redis/vector database.
"""


class MemoryStore:

    def __init__(self):

        self._data = {}

    # ============================================================
    # SAVE
    # ============================================================

    def save(
        self,
        memory
    ):

        self._data[
            memory.key
        ] = memory

    # ============================================================
    # GET
    # ============================================================

    def get(
        self,
        key
    ):

        return self._data.get(
            key
        )

    # ============================================================
    # DELETE
    # ============================================================

    def delete(
        self,
        key
    ):

        return self._data.pop(
            key,
            None
        )

    # ============================================================
    # ALL
    # ============================================================

    def all(self):

        return list(
            self._data.values()
        )

    # ============================================================
    # CLEAR
    # ============================================================

    def clear(self):

        self._data.clear()