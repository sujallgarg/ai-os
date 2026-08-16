from tool_registry.models import (
    ToolDefinition
)

from tools.gmail.read import GmailReader

from tools.gmail.search import GmailSearcher

from tools.gmail.send import GmailSender

from tools.gmail.draft import GmailDraftManager


def register_gmail_tools(
    registry
):

    reader = GmailReader()

    searcher = GmailSearcher()

    sender = GmailSender()

    draft_manager = GmailDraftManager()

    registry.register(
        ToolDefinition(

            name="gmail.read",

            description=(
                "Read a Gmail message."
            ),

            function=reader.get_unread_messages,

            agent_types=[
                "email"
            ],

            requires_approval=False
        )
    )

    registry.register(
        ToolDefinition(

            name="gmail.search",

            description=(
                "Search Gmail messages."
            ),

            function=searcher.search,

            agent_types=[
                "email"
            ],

            requires_approval=False
        )
    )

    registry.register(
        ToolDefinition(

            name="gmail.send",

            description=(
                "Send an email."
            ),

            function=sender.send_email,

            agent_types=[
                "email"
            ],

            requires_approval=True
        )
    )

    registry.register(
        ToolDefinition(

            name="gmail.draft",

            description=(
                "Create a Gmail draft."
            ),

            function=draft_manager.create_draft,

            agent_types=[
                "email"
            ],

            requires_approval=False
        )
    )