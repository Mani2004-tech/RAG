from langsmith import traceable
from agentic_rag.llm.llm_client import LLMClient


class ValidationAgent:

    def __init__(self):

        self.llm = LLMClient()

    @traceable(name="validation_agent")
    def validate(self, query, answer, docs):

        prompt = f"""
Check if the answer is supported by the documents.

Query:
{query}

Answer:
{answer}

Documents:
{docs}

Return:
supported:true/false
"""

        result = self.llm.generate(prompt)

        print("\n🔹 Validation Result:", result)

        return "true" in result.lower()