"""
Error analyzer.
"""


class ErrorAnalyzer:

    RETRYABLE_ERRORS = (
        "timeout",
        "temporarily unavailable",
        "connection",
        "rate limit",
        "429",
        "503"
    )

    USER_ERRORS = (
        "permission denied",
        "authentication",
        "authorization",
        "approval required"
    )

    def analyze(
        self,
        error: str
    ):

        if not error:

            return "UNKNOWN"

        error_lower = (
            error.lower()
        )

        for pattern in self.RETRYABLE_ERRORS:

            if pattern in error_lower:

                return "RETRYABLE"

        for pattern in self.USER_ERRORS:

            if pattern in error_lower:

                return "USER_REQUIRED"

        return "NON_RETRYABLE"