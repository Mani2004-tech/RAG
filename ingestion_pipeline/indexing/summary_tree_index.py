import requests
from config.config import *


class SummaryTreeIndex:

    def generate_summary(self,text):

        prompt=f"""
Summarize the document

{text[:2000]}
"""

        payload={
            "model":MODEL_NAME,
            "prompt":prompt,
            "stream":False
        }

        r=requests.post(
            LLM_ENDPOINT,
            json=payload
        )

        return r.json()["response"]