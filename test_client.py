from tools.gmail.client import GmailClient

client = GmailClient()

service = client.get_service()

print(service)