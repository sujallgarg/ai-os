"""
Policy rules for controlling AI actions.
"""


SENSITIVE_ACTIONS = {

    "send_email",

    "trash_email",

    "delete_email",

    "make_payment",

    "place_trade",

    "purchase",

    "delete_file"
}


SENSITIVE_CATEGORIES = {

    "finance",

    "legal"
}


def is_sensitive_action(
    action: str
):

    return action in SENSITIVE_ACTIONS


def is_sensitive_category(
    category: str
):

    return category in SENSITIVE_CATEGORIES