from retry.manager import (
    RetryManager
)


manager = RetryManager()


print("\nTEST: TIMEOUT")
print("=" * 60)


for i in range(5):

    decision = manager.decide(

        task_id=1,

        error="Connection timeout"
    )

    print(
        f"Attempt {i + 1}"
    )

    print(
        "Retry:",
        decision.should_retry
    )

    print(
        "Attempt:",
        decision.attempt
    )

    print(
        "Delay:",
        round(
            decision.delay,
            2
        )
    )

    print(
        "Reason:",
        decision.reason
    )

    if not decision.should_retry:

        break


print("\nTEST: AUTHENTICATION")
print("=" * 60)


decision = manager.decide(

    task_id=2,

    error="Authentication failed"
)


print(
    "Retry:",
    decision.should_retry
)

print(
    "Reason:",
    decision.reason
)


print("\nTEST: RATE LIMIT")
print("=" * 60)


decision = manager.decide(

    task_id=3,

    error="429 rate limit exceeded"
)


print(
    "Retry:",
    decision.should_retry
)

print(
    "Delay:",
    decision.delay
)