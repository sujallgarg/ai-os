from permissions.models import (
    ToolRequest,
    PermissionDecision
)

from permissions.setup import (
    create_permission_system
)


manager, resolver = (
    create_permission_system()
)


# ============================================================
# TEST 1 — GMAIL SEARCH
# ============================================================

request = ToolRequest(

    agent_id="email",

    tool_name="gmail.search",

    action="search"
)


result = resolver.resolve(
    request
)


print(
    "\nGMAIL SEARCH"
)

print(
    "Decision:",
    result.decision
)

print(
    "Reason:",
    result.reason
)


# ============================================================
# TEST 2 — GMAIL SEND
# ============================================================

request = ToolRequest(

    agent_id="email",

    tool_name="gmail.send",

    action="send"
)


result = resolver.resolve(
    request
)


print(
    "\nGMAIL SEND"
)

print(
    "Decision:",
    result.decision
)

print(
    "Reason:",
    result.reason
)


# ============================================================
# TEST 3 — GMAIL DELETE
# ============================================================

request = ToolRequest(

    agent_id="email",

    tool_name="gmail.delete",

    action="delete"
)


result = resolver.resolve(
    request
)


print(
    "\nGMAIL DELETE"
)

print(
    "Decision:",
    result.decision
)

print(
    "Reason:",
    result.reason
)