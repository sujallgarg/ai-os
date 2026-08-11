from tools.gmail.auth import GmailAuth

auth = GmailAuth()

credentials = auth.authenticate()

print(credentials.valid)