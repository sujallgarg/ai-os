from memory.manager import (
    MemoryManager
)

from memory.shared import (
    SharedMemory
)

from memory.setup import (
    create_default_permissions
)


# ============================================================
# CREATE MEMORY SYSTEM
# ============================================================

permissions = (
    create_default_permissions()
)

manager = MemoryManager(

    permissions=permissions
)


# ============================================================
# EMAIL AGENT
# ============================================================

email_memory = SharedMemory(

    manager,

    "email"
)


# ============================================================
# CODING AGENT
# ============================================================

coding_memory = SharedMemory(

    manager,

    "coding"
)


# ============================================================
# EMAIL AGENT REMEMBERS SOMETHING
# ============================================================

email_memory.remember(

    key="client.theme",

    value="dark",

    memory_type="preference",

    importance=9
)


print(
    "\nEMAIL AGENT"
)

print(
    "Stored client preference."
)


# ============================================================
# CODING AGENT READS IT
# ============================================================

memory = coding_memory.recall(

    "client.theme"
)


print(
    "\nCODING AGENT"
)

print(
    "Client theme:",
    memory.value
)


# ============================================================
# SEARCH
# ============================================================

print(
    "\nSHARED MEMORIES"
)

for memory in coding_memory.search():

    print(

        memory.key,

        "=",

        memory.value
    )