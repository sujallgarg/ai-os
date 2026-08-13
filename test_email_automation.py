from agents.email.classifier import EmailClassifier

from agents.email.automation import (
    EmailAutomationAgent
)


classifier = EmailClassifier()

automation = EmailAutomationAgent()


email = {

    "from": "client@example.com",

    "to": "me@example.com",

    "subject": "Proposal needed",

    "body": """
Hi,

Could you send the revised proposal
tomorrow?

Thanks.
"""
}


classification = classifier.classify(
    email
)


print("\nCLASSIFICATION")
print("=" * 60)

print(
    classification
)


workflows = automation.process(
    email=email,
    classification=classification
)


print("\nWORKFLOWS")
print("=" * 60)

for workflow in workflows:

    print(workflow)