"""
Determines whether an error is retryable.
"""


class RetryPolicy:

    RETRYABLE = {

        "timeout",

        "connection_error",

        "rate_limit",

        "server_error",

        "temporary_error"
    }

    NON_RETRYABLE = {

        "authentication",

        "authorization",

        "invalid_request",

        "validation",

        "permission_denied",

        "user_cancelled"
    }

    def classify(
        self,
        error: str
    ):

        if not error:

            return "unknown"

        error_lower = (
            error.lower()
        )

        # ----------------------------
        # Rate limits
        # ----------------------------

        if (
            "429" in error_lower
            or "rate limit" in error_lower
        ):

            return "rate_limit"

        # ----------------------------
        # Timeouts
        # ----------------------------

        if (
            "timeout" in error_lower
            or "timed out" in error_lower
        ):

            return "timeout"

        # ----------------------------
        # Connection errors
        # ----------------------------

        if (
            "connection" in error_lower
            or "network" in error_lower
        ):

            return "connection_error"

        # ----------------------------
        # Server errors
        # ----------------------------

        if (
            "500" in error_lower
            or "502" in error_lower
            or "503" in error_lower
            or "504" in error_lower
        ):

            return "server_error"

        # ----------------------------
        # Authentication
        # ----------------------------

        if (
            "authentication" in error_lower
            or "unauthorized" in error_lower
            or "401" in error_lower
        ):

            return "authentication"

        # ----------------------------
        # Permission
        # ----------------------------

        if (
            "permission" in error_lower
            or "forbidden" in error_lower
            or "403" in error_lower
        ):

            return "permission_denied"

        # ----------------------------
        # Validation
        # ----------------------------

        if (
            "invalid" in error_lower
            or "validation" in error_lower
        ):

            return "validation"

        return "unknown"

    def is_retryable(
        self,
        error_type: str
    ):

        return (
            error_type
            in self.RETRYABLE
        )