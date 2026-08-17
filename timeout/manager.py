"""
Timeout manager.
"""


class TimeoutManager:

    DEFAULT_TIMEOUTS = {

        "email": 30,

        "browser": 60,

        "coding": 120,

        "calendar": 30,

        "file": 30
    }

    def __init__(
        self,
        default_timeout=30
    ):

        self.default_timeout = (
            default_timeout
        )

    def get_timeout(
        self,
        agent_name: str
    ):

        return self.DEFAULT_TIMEOUTS.get(

            agent_name,

            self.default_timeout
        )

    def set_timeout(
        self,
        agent_name: str,
        timeout_seconds: int
    ):

        if timeout_seconds <= 0:

            raise ValueError(
                "Timeout must be greater than zero."
            )

        self.DEFAULT_TIMEOUTS[
            agent_name
        ] = timeout_seconds