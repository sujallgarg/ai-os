from tools.gmail.label import GmailLabels


labels_manager = GmailLabels()

labels = labels_manager.list_labels()

print("\nGMAIL LABELS")
print("=" * 60)

for label in labels:

    print(
        f"{label['id']} | "
        f"{label['name']} | "
        f"{label['type']}"
    )
