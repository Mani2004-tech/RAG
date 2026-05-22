import requests

from config.config import LLM_ENDPOINT, MODEL_NAME


class SummaryTreeIndex:

    def generate_summary(self, text):
        prompt = f"""
Summarize the document

{text[:2000]}
"""

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(LLM_ENDPOINT, json=payload)
        return response.json()["response"]
