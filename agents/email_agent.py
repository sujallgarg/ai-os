from agents.base_agents import BaseAgent

from tools.gmail.read import GmailReader
from tools.gmail.search import GmailSearcher
from tools.gmail.body import GmailBodyReader
from tools.gmail.thread import GmailThreadReader

from agents.email.summarize import EmailSummarizer
from tools.gmail.label import GmailLabels
from tools.gmail.modify import GmailModifier


class EmailAgent(BaseAgent):

    def __init__(self):

        self.reader = GmailReader()

        self.searcher = GmailSearcher()

        self.body_reader = GmailBodyReader()

        self.thread_reader = GmailThreadReader()

        self.label = GmailLabels()
        self.modifier = GmailModifier()
        self.summarizer = EmailSummarizer()

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
        

        if action == "summarize":

            emails = self.reader.get_unread_messages()

            return self.summarizer.summarize(
                emails
            )

        return self.reader.get_unread_messages()