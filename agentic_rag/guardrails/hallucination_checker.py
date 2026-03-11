from langsmith import traceable
from agentic_rag.llm.llm_client import LLMClient


class HallucinationChecker:

    def __init__(self):

        self.llm = LLMClient()

    @traceable(name="hallucination_check")
    def check(self, query, answer, docs):

        prompt = f"""
Detect hallucination.

Query:
{query}

Answer:
{answer}

Docs:
{docs}
"""

        result = self.llm.generate(prompt)

        return "true" in result.lower()