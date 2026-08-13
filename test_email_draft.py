from tools.gmail.thread import GmailThreadReader
from agents.email.draft_generator import EmailDraftGenerator


thread_reader = GmailThreadReader()

generator = EmailDraftGenerator()


thread_id = input(
    "Enter Gmail thread ID: "
)

instruction = input(
    "What should the reply say? "
)


thread = thread_reader.get_thread(
    thread_id
)


draft = generator.generate_reply(
    thread=thread,
    instruction=instruction
)


print("\n")
print("=" * 60)

print("AI GENERATED DRAFT")

print("=" * 60)

print(draft)

print("=" * 60)
