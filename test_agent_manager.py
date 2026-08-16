from agents.setup import (
    create_agent_manager
)


manager = create_agent_manager()


print("\nREGISTERED AGENTS")
print("=" * 60)

for agent in manager.list_agents():

    print(
        agent
    )