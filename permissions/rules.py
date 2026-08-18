"""
Default permission rules.
"""


DEFAULT_RULES = {

    "email": {

        "gmail.search": "ALLOW",

        "gmail.read": "ALLOW",

        "gmail.draft": "ALLOW",

        "gmail.send": "ASK_USER",

        "gmail.delete": "DENY",
    },

    "coding": {

        "filesystem.read": "ALLOW",

        "filesystem.write": "ALLOW",

        "terminal.execute": "ASK_USER",

        "git.commit": "ASK_USER",

        "git.push": "ASK_USER",

        "filesystem.delete": "ASK_USER",
    },

    "browser": {

        "browser.open": "ALLOW",

        "browser.search": "ALLOW",

        "browser.click": "ALLOW",

        "browser.type": "ALLOW",

        "browser.extract": "ALLOW",

        "browser.download": "ASK_USER",
    },

    "calendar": {

        "calendar.read": "ALLOW",

        "calendar.search": "ALLOW",

        "calendar.create": "ASK_USER",

        "calendar.update": "ASK_USER",

        "calendar.delete": "ASK_USER",
    },

    "file": {

        "file.read": "ALLOW",

        "file.search": "ALLOW",

        "file.write": "ASK_USER",

        "file.delete": "DENY",
    }
}