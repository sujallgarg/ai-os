"""
AI Email Summarizer

Takes emails retrieved from Gmail and asks the LLM
to summarize them in a useful way.
"""

import json 
from llm.provider import LLMProvider

class EmailSummarizer:
    def __init__(self):
        self.llm = LLMProvider()

    def summarize(self, emails):
        if not emails:
            return "You have no unread emails"
        email_data = []
        for email in emails:
            email_data.append(
                f"From: {email.get('from', '')}\n"
                f"Subject: {email.get('subject', '')}\n"
                f"Snippet: {email.get('snippet', '')}"
            )

       
     
        prompt = f"""
You are an intelligent personal email assistant.

Analyze the following unread emails.

Return:

1. A short overall summary
2. Important emails
3. Emails requiring action
4. Emails that can probably be ignored

Keep the response concise and useful.

Emails:

{json.dumps(email_data, indent=2)}
"""

        messages = [
            {
                "role": "system",
                "content": "You are a helpful email management assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        return self.llm.chat(messages)
            
       