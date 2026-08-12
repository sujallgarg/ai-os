from tools.gmail.body import GmailBodyReader


reader = GmailBodyReader()

message_id = input(
    "Enter Gmail message ID: "
)

email = reader.get_email(
    message_id
)

print("\n" + "=" * 60)

print("FROM:")
print(email["from"])

print("\nTO:")
print(email["to"])

print("\nSUBJECT:")
print(email["subject"])

print("\nDATE:")
print(email["date"])

print("\nBODY:")
print(email["body"])

print("=" * 60)