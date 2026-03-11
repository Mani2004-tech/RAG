import requests
import json
from config.config import LLM_ENDPOINT, MODEL_NAME, MAX_LLM_INPUT


class MetadataExtractor:

    def extract(self, text):

        text = text[:MAX_LLM_INPUT]

        prompt = f"""
Analyze this document text.

Return JSON:

{{
 "keywords": [],
 "topic": "",
 "summary": ""
}}

TEXT:
{text}
"""

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(LLM_ENDPOINT, json=payload)

        data = response.json()

        try:

            result = json.loads(data["response"])

        except:

            result = {
                "keywords": [],
                "topic": "",
                "summary": ""
            }

        return result