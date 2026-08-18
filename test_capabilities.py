from agents.capabilities.registry import (
    CapabilityRegistry
)

from agents.capabilities.matcher import (
    CapabilityMatcher
)

from agents.capabilities.defaults import (
    register_default_agents
)


registry = CapabilityRegistry()

register_default_agents(
    registry
)


matcher = CapabilityMatcher(
    registry
)


# ============================================================
# TEST 1
# ============================================================

agent = matcher.find_best_agent(

    [
        "email.search"
    ]
)


print(
    "\nEMAIL SEARCH"
)

print(
    "Best agent:",
    agent.name
)


# ============================================================
# TEST 2
# ============================================================

agent = matcher.find_best_agent(

    [
        "code.write",
        "code.test"
    ]
)


print(
    "\nCODE TASK"
)

print(
    "Best agent:",
    agent.name
)


# ============================================================
# TEST 3
# ============================================================

agent = matcher.find_best_agent(

    [
        "browser.open",
        "browser.click"
    ]
)


print(
    "\nBROWSER TASK"
)

print(
    "Best agent:",
    agent.name
)
