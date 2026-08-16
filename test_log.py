from logs.service import (
    ExecutionLogService
)


service = ExecutionLogService()


USER_ID = "demo-user"


log = service.start(

    task_id=1,

    user_id=USER_ID,

    agent="email",

    action="search",

    tool="gmail.search"
)


print(
    "Started:",
    log
)


result = service.complete(

    log,

    output={
        "emails_found": 3
    },

    policy_decision="ALLOW"
)


print(
    "\nCompleted:"
)

print(
    result
)


history = service.history(
    USER_ID
)


print(
    "\nEXECUTION HISTORY"
)

print(
    "=" * 60
)


for row in history:

    print(row)