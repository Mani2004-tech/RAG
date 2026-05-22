import requests
from langsmith import traceable

from agentic_rag.config.config import LLM_ENDPOINT, MODEL_NAME


class LLMClient:

    @traceable(name="llm_call")
    def generate(self, prompt):
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(LLM_ENDPOINT, json=payload)
        return response.json()["response"]
