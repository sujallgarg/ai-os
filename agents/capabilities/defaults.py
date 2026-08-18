"""
Default agent capability definitions.
"""


from agents.capabilities.models import (
    AgentProfile
)


def register_default_agents(
    registry
):

    # ============================================================
    # EMAIL AGENT
    # ============================================================

    registry.register(

        AgentProfile(

            name="email",

            description=(
                "Handles email workflows."
            ),

            capabilities=[

                "email.read",

                "email.search",

                "email.draft",

                "email.reply"
            ],

            tools=[

                "gmail.search",

                "gmail.read",

                "gmail.draft"
            ],

            priority=8
        )
    )

    # ============================================================
    # CODING AGENT
    # ============================================================

    registry.register(

        AgentProfile(

            name="coding",

            description=(
                "Writes, modifies and tests code."
            ),

            capabilities=[

                "code.read",

                "code.write",

                "code.modify",

                "code.test",

                "code.debug",

                "git.commit"
            ],

            tools=[

                "filesystem",

                "terminal",

                "git"
            ],

            priority=9
        )
    )

    # ============================================================
    # BROWSER AGENT
    # ============================================================

    registry.register(

        AgentProfile(

            name="browser",

            description=(
                "Interacts with websites."
            ),

            capabilities=[

                "browser.open",

                "browser.search",

                "browser.click",

                "browser.type",

                "browser.extract",

                "browser.test"
            ],

            tools=[

                "playwright"
            ],

            priority=8
        )
    )

    # ============================================================
    # CALENDAR AGENT
    # ============================================================

    registry.register(

        AgentProfile(

            name="calendar",

            description=(
                "Handles calendar workflows."
            ),

            capabilities=[

                "calendar.read",

                "calendar.search",

                "calendar.create",

                "calendar.update"
            ],

            tools=[

                "google_calendar"
            ],

            priority=7
        )
    )

    # ============================================================
    # FILE AGENT
    # ============================================================

    registry.register(

        AgentProfile(

            name="file",

            description=(
                "Handles local and cloud files."
            ),

            capabilities=[

                "file.read",

                "file.write",

                "file.search",

                "file.move",

                "file.delete"
            ],

            tools=[

                "filesystem",

                "google_drive"
            ],

            priority=7
        )
    )

    return registry