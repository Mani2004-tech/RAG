from langsmith import traceable
from agentic_rag.llm.llm_client import LLMClient
import json


class QueryDecomposer:

    def __init__(self):

        print("🧩 Query Decomposer initialized")

        self.llm = LLMClient()
    @traceable(name="query_decomposer", run_type="llm")
    def run(self, query, plan):

        if plan.get("query_complexity") != "multi-hop":

            return [query]

        prompt = f"""
Break the query into smaller sub-queries for retrieval.

Query:
{query}

Return JSON list:

subqueries:[]
"""

        response = self.llm.generate(prompt)

        try:
            data = json.loads(response)

            subqueries = data.get("subqueries", [])

            if not subqueries:
                subqueries = [query]

        except Exception:

            subqueries = [query]

        print("\n🧩 Decomposed Queries:", subqueries)

        return subqueries