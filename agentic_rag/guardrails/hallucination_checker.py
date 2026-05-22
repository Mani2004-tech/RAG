import json

from langsmith import traceable

from agentic_rag.llm.llm_client import LLMClient


class HallucinationChecker:

    def __init__(self):
        self.llm = LLMClient()

    @traceable(name="hallucination_check")
    def check(self, query, answer, docs):
        context = ""
        for i, d in enumerate(docs[:5]):
            context += f"\nDoc{i+1}: {d.content[:400]}"

        prompt = f"""
Determine if the answer contains hallucination.

Query:
{query}

Answer:
{answer}

Documents:
{context}

Return JSON:

hallucination:true/false
"""

        result = self.llm.generate(prompt)

        try:
            data = json.loads(result)
            return data.get("hallucination", False)
        except Exception:
            return False
