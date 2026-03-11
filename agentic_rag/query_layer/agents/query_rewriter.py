from agentic_rag.llm.llm_client import LLMClient
from langsmith import traceable


class QueryRewriter:

    def __init__(self):
        self.llm = LLMClient()

    @traceable(name="query_rewrite")
    def run(self, query):

        print("\n🔹 Original Query:", query)

        prompt = f"""
Rewrite the user query to improve retrieval quality.

User Query:
{query}

Return only the rewritten query.
"""

        rewritten = self.llm.generate(prompt)

        print("🔹 Rewritten Query:", rewritten)

        return rewritten