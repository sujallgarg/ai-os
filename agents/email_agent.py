from agents.base_agents import BaseAgent

from tools.gmail.read import GmailReader
from tools.gmail.search import GmailSearcher
from tools.gmail.body import GmailBodyReader

from agents.email.summarize import EmailSummarizer


class EmailAgent(BaseAgent):

    def __init__(self):

        self.reader = GmailReader()

        self.searcher = GmailSearcher()

        self.body_reader = GmailBodyReader()

        self.summarizer = EmailSummarizer()

    def execute(self, task):

        action = task.get(
            "action",
            "read"
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

        if action == "summarize":

            emails = self.reader.get_unread_messages()

            return self.summarizer.summarize(
                emails
            )

        return self.reader.get_unread_messages()