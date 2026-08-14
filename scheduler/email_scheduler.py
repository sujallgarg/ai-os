"""
Background Email Agent Scheduler.

Periodically checks Gmail for new messages,
classifies them, and evaluates automation workflows.
"""

import time

from agents.email.classifier import EmailClassifier
from agents.email.automation import EmailAutomationAgent

from tools.gmail.search import GmailSearcher
from tools.gmail.body import GmailBodyReader

from scheduler.state import SchedulerState


class EmailScheduler:

    def __init__(
        self,
        interval_seconds=300
    ):

        self.interval_seconds = (
            interval_seconds
        )

        self.searcher = GmailSearcher()

        self.body_reader = GmailBodyReader()

        self.classifier = EmailClassifier()

        self.automation = (
            EmailAutomationAgent()
        )

        self.state = SchedulerState()

        self.running = False

    def process_new_emails(self):

        print(
            "\n[Email Scheduler] "
            "Checking Gmail..."
        )

        emails = self.searcher.search(
            query="is:unread",
            limit=20
        )

        print(
            f"[Email Scheduler] "
            f"Found {len(emails)} unread emails."
        )

        new_emails = [
            e for e in emails if not self.state.is_processed(e.get("id"))
        ]

        if not new_emails:
            print(
                "[Email Scheduler] "
                "All unread emails have already been processed in previous runs."
            )
            return

        print(
            f"[Email Scheduler] "
            f"Processing {len(new_emails)} new email(s)..."
        )

        for email_summary in new_emails:

            message_id = email_summary.get(
                "id"
            )

            if not message_id:
                continue

            try:

                self.process_email(
                    message_id
                )

                self.state.mark_processed(
                    message_id
                )

            except Exception as error:

                print(
                    "[Email Scheduler] "
                    f"Error processing {message_id}: "
                    f"{error}"
                )

            time.sleep(1.5)



    def process_email(
        self,
        message_id: str
    ):

        print(
            f"[Email Scheduler] "
            f"Processing {message_id}"
        )

        email = self.body_reader.get_email(
            message_id
        )

        classification = (
            self.classifier.classify(
                email
            )
        )

        print(
            "[Email Scheduler] "
            "Classification:"
        )

        print(
            classification
        )

        workflows = (
            self.automation.process(
                email=email,
                classification=classification
            )
        )

        if not workflows:

            print(
                "[Email Scheduler] "
                "No workflow matched."
            )

            return

        for workflow in workflows:

            print(
                "[Email Scheduler] "
                f"Matched: {workflow}"
            )

    def start(self):

        self.running = True

        print(
            "[Email Scheduler] Started."
        )

        print(
            f"[Email Scheduler] "
            f"Interval: {self.interval_seconds} seconds"
        )

        while self.running:

            try:

                self.process_new_emails()

            except Exception as error:

                print(
                    "[Email Scheduler] "
                    f"Scheduler error: {error}"
                )

            if not self.running:

                break

            print(
                f"[Email Scheduler] "
                f"Sleeping for "
                f"{self.interval_seconds} seconds..."
            )

            time.sleep(
                self.interval_seconds
            )

    def stop(self):

        self.running = False

        print(
            "[Email Scheduler] Stopping..."
        )