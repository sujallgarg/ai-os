"""
Default memory permission configuration.
"""

from memory.permissions import (
    MemoryPermissionManager
)


def create_default_permissions():

    permissions = (
        MemoryPermissionManager()
    )

    # ============================================================
    # EMAIL AGENT
    # ============================================================

    permissions.allow(
        "email",
        "shared"
    )

    permissions.allow(
        "email",
        "goal"
    )

    permissions.allow(
        "email",
        "task"
    )

    permissions.allow(
        "email",
        "preference"
    )

    permissions.allow(
        "email",
        "result"
    )

    # ============================================================
    # CODING AGENT
    # ============================================================

    permissions.allow(
        "coding",
        "shared"
    )

    permissions.allow(
        "coding",
        "goal"
    )

    permissions.allow(
        "coding",
        "task"
    )

    permissions.allow(
        "coding",
        "preference"
    )

    permissions.allow(
        "coding",
        "result"
    )

    # ============================================================
    # BROWSER AGENT
    # ============================================================

    permissions.allow(
        "browser",
        "shared"
    )

    permissions.allow(
        "browser",
        "goal"
    )

    permissions.allow(
        "browser",
        "task"
    )

    permissions.allow(
        "browser",
        "preference"
    )

    permissions.allow(
        "browser",
        "result"
    )

    # ============================================================
    # SUPERVISOR
    # ============================================================

    permissions.allow(
        "supervisor",
        "shared"
    )

    permissions.allow(
        "supervisor",
        "goal"
    )

    permissions.allow(
        "supervisor",
        "task"
    )

    permissions.allow(
        "supervisor",
        "preference"
    )

    permissions.allow(
        "supervisor",
        "result"
    )

    return permissions