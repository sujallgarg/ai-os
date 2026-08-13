from agents.base_agents import BaseAgent

from tools.gmail.read import GmailReader
from tools.gmail.search import GmailSearcher
from tools.gmail.body import GmailBodyReader
from tools.gmail.thread import GmailThreadReader
from agents.email.draft_generator import EmailDraftGenerator
from agents.email.summarize import EmailSummarizer
from tools.gmail.label import GmailLabels
from tools.gmail.modify import GmailModifier
from tools.gmail.draft import GmailDraftManager
from security.approval import ApprovalManager
from tools.gmail.send import GmailSender

class EmailAgent(BaseAgent):

    def __init__(self):

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

    def execute(self, task):

        action = task.get(
            "action",
            "read"
        )

        if action == "labels":

            return self.label.list_labels()
            
        if action == "label_search":
            
            label = task.get(
                "label",
                ""
            ) 
            
            return self.searcher.search_by_label(
                label=label
            )

        if action == "search":

            query = task.get(
                "query",
                ""
            )

            return self.searcher.search(
                query
            )

        if action == "read":

            message_id = task.get(
                "message_id"
            )

            if message_id:

                return self.body_reader.get_email(
                    message_id
                )

            return self.reader.get_unread_messages()

        if action == "thread":

            thread_id = task.get(
                "thread_id"
            )

            return self.thread_reader.get_thread(
                thread_id
            )
            
        if action == "mark_read":
            message_id = task.get(
                "message_id"
            )
            return self.modifier.mark_as_read(
                message_id
            )
        if action == "mark_unread":
            message_id = task.get(
                "message_id"
            )
            return self.modifier.mark_as_unread(
                message_id
            )
        if action == "archive":
            message_id = task.get(
                "message_id"
            )
            return self.modifier.archive(
                message_id
            )
        if action == "trash":

            message_id = task.get(
                "message_id"
            )

            request = self.approval.create_request(
                action="trash_email",
                description="Move email to trash",
                data={
                    "message_id": message_id
                }
            )

            return request

        if action == "summarize":

            emails = self.reader.get_unread_messages()

            return self.summarizer.summarize(
                emails
            )
            

        return self.reader.get_unread_messages()

        if action == "draft_reply":

            thread_id = task.get(
                "thread_id"
            )

            instruction = task.get(
                "instruction"
        )

        thread = self.thread_reader.get_thread(
            thread_id
        )

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

            request = self.approval.create_request(
        action="send_email",
        description="Send an email",
        data={
            "to": task.get("to"),
            "subject": task.get("subject"),
            "body": task.get("body"),
            "thread_id": task.get("thread_id"),
            "in_reply_to": task.get(
                "in_reply_to"
            ),
            "references": task.get(
                "references"
            )
        }
    )

        return request