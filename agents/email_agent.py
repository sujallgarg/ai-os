from agents.base_agents import BaseAgent

from tools.gmail.read import GmailReader
from agents.email.summarize import EmailSummarizer


class EmailAgent(BaseAgent):

    def __init__(self):

        self.reader = GmailReader()

        self.summarizer = EmailSummarizer()

    def execute(self, task):

        emails = self.reader.get_unread_messages()

        summary = self.summarizer.summarize(emails)

        return summary