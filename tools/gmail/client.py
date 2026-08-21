"""
Creates a reusable Gmail API client.

Every Gmail operation should use this client.
"""

from googleapiclient.discovery import build 
from tools.gmail.auth import GmailAuth


class GmailClient:
    def __init__(self):
        self.auth = GmailAuth()
        self.service = None
    
    def connect(self):
        try:
            credentials = self.auth.authenticate()
            self.service = build(
                "gmail",
                "v1",
                credentials=credentials
            )
            return self.service
        except Exception as error:
            print(f"[GmailClient] Authentication warning: {error}")
            return None

    def get_service(self):
        if self.service is None:
            return self.connect()
        return self.service


_client_instance = GmailClient()
service = None