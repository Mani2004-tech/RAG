from langsmith import traceable
from agentic_rag.llm.llm_client import LLMClient



class LLMReranker:

    def __init__(self):
        self.llm = LLMClient()

    @traceable(name="llm_reranker")
    def rerank(self, query, docs):

        docs = docs[:5]  # ✅ LIMIT to avoid too many LLM calls
        scored = []

        for d in docs:

            prompt = f"""
Score relevance from 1 to 10.

Query:
{query}

Document:
{d.content}
"""

            import re

            score_text = self.llm.generate(prompt)

            match = re.search(r"\d+(\.\d+)?", score_text)

            score = float(match.group()) if match else 0.0

            scored.append((score, d))

        scored.sort(key=lambda x: x[0], reverse=True)



        return [d for _, d in scored]