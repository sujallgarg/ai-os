import json
import re


class JsonParser:
    def parse(self, text):
        if isinstance(text, dict):
            return text
        if not isinstance(text, str):
            return {"task": str(text), "intent": str(text)}

        # Strip markdown ```json ... ``` blocks if present
        clean_text = text.strip()
        if clean_text.startswith("```"):
            clean_text = re.sub(r"^```(?:json)?\s*", "", clean_text)
            clean_text = re.sub(r"\s*```$", "", clean_text)

        try:
            return json.loads(clean_text)
        except Exception:
            return {"task": text, "intent": text}

    def parser(self, text):
        return self.parse(text)