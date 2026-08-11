"""
Google OAuth Authentication

Handles user login and stores OAuth tokens.
"""

from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES=[
    "https://www.googleapis.com/auth/gmail.readonly"
    ]

TOKEN_FILE = Path("token.json")


def get_credentials_file() -> Path:
    if Path("credentials.json").exists():
        return Path("credentials.json")
    client_secrets = list(Path(".").glob("client_secret_*.json"))
    if client_secrets:
        return client_secrets[0]
    return Path("credentials.json")


class GmailAuth:

    def authenticate(self):
        creds = None

        # Load existing token
        if TOKEN_FILE.exists():
            creds = Credentials.from_authorized_user_file(
                TOKEN_FILE,
                SCOPES
            )

        # Refresh token if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # First Login
        elif not creds or not creds.valid:
            cred_file = get_credentials_file()
            if not cred_file.exists():
                raise FileNotFoundError(
                    f"Credentials file '{cred_file}' not found. "
                    "Please download your OAuth client credentials from Google Cloud Console "
                    "and place it as 'credentials.json' in the project root."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                cred_file,
                SCOPES
            )

            creds = flow.run_local_server(port=0)

            TOKEN_FILE.write_text(
                creds.to_json()
            )

        return creds