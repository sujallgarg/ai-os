from planner.planner import Planner
from memory.memory import Memory
from agents.agent_manager import AgentManager
from app.display import show_banner, display_result, console

memory = Memory()
agents = AgentManager()
planner = Planner(memory, agents)

show_banner()

while True:
    try:
        task = console.input("\n[bold bright_cyan]ai-os[/bold bright_cyan] [bold white]❯[/bold white] ").strip()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[dim]Exiting AI OS. Goodbye![/dim]")
        break

    if not task:
        continue

    if task.lower() in ("exit", "quit"):
        console.print("[dim]Exiting AI OS. Goodbye![/dim]")
        break

    result = planner.run(task)
    display_result(result)