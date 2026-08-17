from agents.registry.models import (
    AgentDefinition
)


def register_default_agents(
    registry
):

    registry.register(

        AgentDefinition(

            name="email",

            description=(
                "Handles Gmail and "
                "email-related tasks."
            ),

            capabilities=[

                "gmail.read",

                "gmail.search",

                "gmail.draft",

                "gmail.send",

                "gmail.reply",

                "gmail.forward"

            ],

            version="1.0.0"
        )
    )