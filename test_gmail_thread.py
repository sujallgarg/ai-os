from tools.gmail.thread import GmailThreadReader


reader = GmailThreadReader()

thread_id = input(
    "Enter Gmail thread ID: "
)

thread = reader.get_thread(
    thread_id
)

print("\n")
print("=" * 70)

print("THREAD ID:")
print(thread["thread_id"])

print("\nMESSAGE COUNT:")
print(thread["message_count"])

print("=" * 70)

for index, message in enumerate(
    thread["messages"],
    start=1
):

    print(f"\nMESSAGE {index}")

    print("-" * 70)

    print("FROM:")
    print(message["from"])

    print("\nTO:")
    print(message["to"])

    print("\nSUBJECT:")
    print(message["subject"])

    print("\nDATE:")
    print(message["date"])

    print("\nBODY:")
    print(message["body"])

    print("-" * 70)