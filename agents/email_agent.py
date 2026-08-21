from agents.base_agents import BaseAgent
from tools.gmail.read import GmailReader
from tools.gmail.search import GmailSearcher
from tools.gmail.body import GmailBodyReader
from tools.gmail.thread import GmailThreadReader
from tools.gmail.label import GmailLabels
from tools.gmail.modify import GmailModifier
from tools.gmail.draft import GmailDraftManager
from tools.gmail.send import GmailSender
from tools.gmail.attachments import GmailAttachmentManager
from agents.email.draft_generator import EmailDraftGenerator
from agents.email.summarize import EmailSummarizer
from agents.email.classifier import EmailClassifier
from security.approval import ApprovalManager


class EmailAgent(BaseAgent):

    def __init__(self):
        super().__init__()
        self.name = "email"
        self.description = "Handles Gmail and email-related operations."
        self.capabilities = [
            "gmail.read",
            "gmail.search",
            "gmail.draft",
            "gmail.send",
            "gmail.reply",
            "gmail.forward"
        ]
        self.reader = GmailReader()
        self.searcher = GmailSearcher()
        self.body_reader = GmailBodyReader()
        self.thread_reader = GmailThreadReader()
        self.labels = GmailLabels()
        self.modifier = GmailModifier()
        self.summarizer = EmailSummarizer()
        self.draft_generator = EmailDraftGenerator()
        self.draft_manager = GmailDraftManager()
        self.approval = ApprovalManager()
        self.sender = GmailSender()
        self.attachments = GmailAttachmentManager()
        self.classifier = EmailClassifier()

    def execute(self, task: dict):
        action = task.get("action", "read")

        if action == "labels":
            return self.labels.list_labels()

        if action == "label_search":
            label = task.get("label", "")
            return self.searcher.search_by_label(label=label)

        if action == "search":
            query = task.get("query", "")
            return self.searcher.search(query)

        if action == "read":
            message_id = task.get("message_id")
            if message_id:
                return self.body_reader.get_email(message_id)
            return self.reader.get_unread_messages()

        if action == "thread":
            thread_id = task.get("thread_id")
            return self.thread_reader.get_thread(thread_id)

        if action == "mark_read":
            message_id = task.get("message_id")
            return self.modifier.mark_as_read(message_id)

        if action == "mark_unread":
            message_id = task.get("message_id")
            return self.modifier.mark_as_unread(message_id)

        if action == "archive":
            message_id = task.get("message_id")
            return self.modifier.archive(message_id)

        if action == "trash":
            message_id = task.get("message_id")
            return self.approval.create_request(
                action="trash_email",
                description="Move email to trash",
                data={"message_id": message_id}
            )

        if action == "summarize":
            emails = self.reader.get_unread_messages()
            return self.summarizer.summarize(emails)

        if action == "draft_reply":
            thread_id = task.get("thread_id")
            instruction = task.get("instruction", "Generate polite executive reply.")
            thread = self.thread_reader.get_thread(thread_id) if thread_id else {}
            draft = self.draft_generator.generate_reply(
                thread=thread,
                instruction=instruction
            )
            return {
                "thread_id": thread_id,
                "action": "draft_reply",
                "draft": draft
            }

        if action == "create_draft":
            to = task.get("to")
            subject = task.get("subject")
            body = task.get("body")
            thread_id = task.get("thread_id")
            return self.draft_manager.create_draft(
                to=to,
                subject=subject,
                body=body,
                thread_id=thread_id
            )

        if action == "send_email":
            return self.approval.create_request(
                action="send_email",
                description=f"Send email to {task.get('to')}",
                data={
                    "to": task.get("to"),
                    "subject": task.get("subject"),
                    "body": task.get("body"),
                    "thread_id": task.get("thread_id"),
                    "in_reply_to": task.get("in_reply_to"),
                    "references": task.get("references")
                }
            )

        if action == "reply":
            return self.approval.create_request(
                action="send_email",
                description="Reply to an existing Gmail conversation",
                data={
                    "to": task.get("to"),
                    "subject": task.get("subject"),
                    "body": task.get("body"),
                    "thread_id": task.get("thread_id"),
                    "in_reply_to": task.get("in_reply_to"),
                    "references": task.get("references")
                }
            )

        if action == "forward":
            message_id = task.get("message_id")
            to = task.get("to")
            additional_message = task.get("message", "")
            original_email = self.body_reader.get_email(message_id) if message_id else {}
            draft = self.draft_manager.create_forward_draft(
                to=to,
                original_email=original_email,
                additional_message=additional_message
            )
            return {
                "status": "draft_created",
                "action": "forward",
                "draft": draft
            }

        if action == "attachments":
            message_id = task.get("message_id")
            return self.attachments.list_attachments(message_id)

        if action == "download_attachment":
            message_id = task.get("message_id")
            attachment_id = task.get("attachment_id")
            filename = task.get("filename")
            return self.attachments.download_attachment(
                message_id=message_id,
                attachment_id=attachment_id,
                filename=filename
            )

        if action == "classify":
            message_id = task.get("message_id")
            email = self.body_reader.get_email(message_id) if message_id else {}
            classification = self.classifier.classify(email)
            return {
                "message_id": message_id,
                "classification": classification
            }

        return self.reader.get_unread_messages()