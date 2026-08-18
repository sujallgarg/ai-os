"""
Create the default permission system.
"""

from permissions.rules import (
    DEFAULT_RULES
)

from permissions.manager import (
    PermissionManager
)

from permissions.resolver import (
    PermissionResolver
)


def create_permission_system():

    manager = PermissionManager(

        rules=DEFAULT_RULES
    )

    resolver = PermissionResolver(

        manager
    )

    return manager, resolver