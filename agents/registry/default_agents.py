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

    registry.register(

        AgentDefinition(

            name="coding",

            description=(
                "Handles software development, "
                "code generation, and debugging."
            ),

            capabilities=[

                "code.generate",

                "code.review",

                "code.debug",

                "code.execute"

            ],

            version="1.0.0"
        )
    )

    registry.register(

        AgentDefinition(

            name="browser",

            description=(
                "Performs web searches, browsing, "
                "and information extraction."
            ),

            capabilities=[

                "web.search",

                "web.browse",

                "web.extract"

            ],

            version="1.0.0"
        )
    )

    registry.register(

        AgentDefinition(

            name="calendar",

            description=(
                "Manages schedule, meetings, "
                "and calendar events."
            ),

            capabilities=[

                "calendar.view",

                "calendar.create",

                "calendar.update"

            ],

            version="1.0.0"
        )
    )

    registry.register(

        AgentDefinition(

            name="file",

            description=(
                "Manages local files and "
                "document processing."
            ),

            capabilities=[

                "file.read",

                "file.write",

                "file.search"

            ],

            version="1.0.0"
        )
    )