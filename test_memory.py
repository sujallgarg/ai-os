from memory.manager import MemoryManager
from memory.search import MemorySearch


manager = MemoryManager()


USER_ID = "demo-user"


memory = manager.remember(

    user_id=USER_ID,

    memory_type="preference",

    key="email_tone",

    value="professional and concise",

    importance=0.9
)


print("\nMEMORY SAVED")
print("=" * 60)

print(
    memory
)


memories = manager.get_user_memories(
    USER_ID
)


print("\nUSER MEMORIES")
print("=" * 60)

for item in memories:

    print(item)


search = MemorySearch()


results = search.search(
    memories,
    "email tone"
)


print("\nSEARCH RESULTS")
print("=" * 60)

for result in results:

    print(result)