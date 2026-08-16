from policy.preferences import (
    UserPreferenceManager
)


manager = UserPreferenceManager()


preferences = manager.load()


preferences["email"][
    "auto_reply_enabled"
] = True


preferences["email"][
    "auto_reply_max_priority"
] = "medium"


manager.update(
    preferences
)


print(
    "Preferences updated."
)


print(
    manager.load()
)