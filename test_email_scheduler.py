from scheduler.email_scheduler import EmailScheduler


if __name__ == "__main__":
    scheduler = EmailScheduler(interval_seconds=60)
    print("Testing Email Scheduler...")
    scheduler.process_new_emails()
