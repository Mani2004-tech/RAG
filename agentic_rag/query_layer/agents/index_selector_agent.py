from langsmith import traceable
from agentic_rag.llm.llm_client import LLMClient


class IndexSelectorAgent:

    def __init__(self):
        self.llm = LLMClient()

    @traceable(name="index_selector", run_type="llm")
    def run(self, query, plan):
        print("\n🔹 Index Selector Input:", query)
        prompt = f"""
Select the best index for retrieval.

Available indexes:
vector
bm25
hybrid
parent_child
temporal

Query:
{query}

Plan:
{plan}

Return only the index name.
"""
        print("\n🔹 Index Selector Input:", query)
        return self.llm.generate(prompt).strip()