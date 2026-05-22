from agentic_rag.llm.llm_client import LLMClient


class IndexSelectorAgent:

    def __init__(self):
        self.llm = LLMClient()

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

        return self.llm.generate(prompt).strip()
