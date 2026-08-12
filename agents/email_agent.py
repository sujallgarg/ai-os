from agents.base_agents import BaseAgent

from tools.gmail.read import GmailReader
from tools.gmail.search import GmailSearcher

from agents.email.summarize import EmailSummarizer


class EmailAgent(BaseAgent):

    def __init__(self):

        self.reader = GmailReader()

        self.searcher = GmailSearcher()

        self.summarizer = EmailSummarizer()

    def execute(self, task):

        action = task.get("action", "read")

        if action == "search":

            query = task.get("query", "")

            return self.searcher.search(query)

        if action == "summarize":

            emails = self.reader.get_unread_messages()

            return self.summarizer.summarize(emails)

        return self.reader.get_unread_messages()