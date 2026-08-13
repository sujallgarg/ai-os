from agents.email.classifier import EmailClassifier


classifier = EmailClassifier()


email = {

    "from": "john@example.com",

    "to": "you@example.com",

    "subject": "Need the proposal tomorrow",

    "body": """
Hi,

We're still waiting for the revised proposal.

Could you send it by tomorrow?

Thanks,
John
"""
}


result = classifier.classify(
    email
)


print("\nAI CLASSIFICATION")
print("=" * 60)

for key, value in result.items():

    print(
        f"{key}: {value}"
    )

print("=" * 60)