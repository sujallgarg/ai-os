from planner.planner import Planner
from memory.memory import Memory
from agents.agent_manager import AgentManager

memory = Memory()
agents=AgentManager()
planner = Planner(memory,agents)

print("AI OS Started 🚀")




while True:

    task = input("\n>>> ")

    if task == "exit":
        break

    result = planner.run(task)

    print(result)