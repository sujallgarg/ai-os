from policy.preferences import (
    UserPreferenceManager
)


manager = UserPreferenceManager()


preferences = manager.load()


print("\nUSER PREFERENCES")
print("=" * 60)

print(preferences)
