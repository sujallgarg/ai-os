import html
import re
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def clean_text(text: str) -> str:
    """Clean HTML entities, zero-width characters, and extra spaces."""
    if not isinstance(text, str):
        return str(text)
    unescaped = html.unescape(text)
    cleaned = re.sub(r"[\ufeff\u200b\u200c\u200d\u034f]", "", unescaped)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def show_banner():
    """Display an attractive startup banner."""
    banner_content = (
        "[bold bright_cyan]⚡ AI OS[/bold bright_cyan] [dim]| Autonomous Agent System[/dim]\n\n"
        "[green]●[/green] [bold]Groq LLM[/bold] (Llama 3.3 70B)  "
        "[green]●[/green] [bold]Gmail API[/bold] (Connected)  "
        "[green]●[/green] [bold]Vector Memory[/bold] (Active)\n"
        "[dim]Type your task below (e.g. 'read all unread emails') or 'exit' to quit.[/dim]"
    )
    console.print(
        Panel(
            banner_content,
            border_style="bright_blue",
            title="🚀 [bold white]System Initialized[/bold white]",
            subtitle="[dim]Ready for commands[/dim]",
            expand=False,
            padding=(1, 2),
        )
    )


def display_emails(emails: list):
    """Render emails in a sleek, readable table."""
    if not emails:
        console.print(
            Panel(
                "[yellow]📭 No unread emails found in your inbox.[/yellow]",
                border_style="yellow",
                expand=False,
                padding=(0, 2),
            )
        )
        return

    table = Table(
        title=f"\n📬 [bold bright_cyan]Unread Emails[/bold bright_cyan] [dim]({len(emails)} total)[/dim]",
        border_style="bright_blue",
        header_style="bold bright_white on blue",
        show_lines=True,
        expand=True,
    )

    table.add_column("#", style="bold yellow", justify="center", width=4)
    table.add_column("From", style="bright_cyan", width=26, overflow="ellipsis")
    table.add_column("Subject", style="bold white", width=34, overflow="fold")
    table.add_column("Preview", style="dim white", overflow="fold")

    for idx, msg in enumerate(emails, start=1):
        sender = clean_text(msg.get("from", "Unknown"))
        subject = clean_text(msg.get("subject", "(No Subject)"))
        snippet = clean_text(msg.get("snippet", ""))

        table.add_row(
            f"[bold yellow]{idx}[/bold yellow]",
            sender,
            subject,
            snippet,
        )

    console.print(table)


def clean_item(item):
    """Recursively clean strings in dicts, lists, and primitives."""
    if isinstance(item, str):
        return clean_text(item)
    elif isinstance(item, dict):
        return {k: clean_item(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [clean_item(x) for x in item]
    return item


def display_result(result):
    """Format and print output as structured, highlighted JSON."""
    import json

    cleaned = clean_item(result)

    # If already a JSON string, deserialize first
    if isinstance(cleaned, str):
        try:
            cleaned = json.loads(cleaned)
        except Exception:
            cleaned = {"output": cleaned}

    # Structure into clean JSON payload
    if isinstance(cleaned, list):
        payload = {
            "status": "success",
            "count": len(cleaned),
            "data": cleaned,
        }
    elif isinstance(cleaned, dict):
        payload = cleaned
    else:
        payload = {"status": "success", "result": cleaned}

    json_str = json.dumps(payload, indent=2, ensure_ascii=False)
    console.print_json(json_str)

