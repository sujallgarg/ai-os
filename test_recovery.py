from recovery.manager import (
    RecoveryManager
)


manager = RecoveryManager(
    max_retries=3
)


print("\nTEST 1 — TIMEOUT")
print("=" * 60)


for i in range(4):

    result = manager.handle_failure(

        task_id=1,

        error="Connection timeout"
    )

    print(
        f"Attempt {i + 1}:",
        result
    )


print("\nTEST 2 — PERMISSION")
print("=" * 60)


result = manager.handle_failure(

    task_id=2,

    error="Permission denied"
)


print(result)


print("\nTEST 3 — UNKNOWN ERROR")
print("=" * 60)


result = manager.handle_failure(

    task_id=3,

    error="Invalid project configuration"
)


print(result)