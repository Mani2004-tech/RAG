from langsmith import traceable
from agentic_rag.llm.llm_client import LLMClient
import json


class HallucinationChecker:

    def __init__(self):

        self.llm = LLMClient()

    @traceable(name="hallucination_check")
    def check(self, query, answer, docs):
       
        context = ""

        for i,d in enumerate(docs[:5]):
            context += f"\nDoc{i+1}: {d.content[:400]}"

        prompt = f"""
Determine if the answer contains hallucination.

Return ONLY valid JSON:

{{ "hallucination": true/false }}

Query:
{query}

Answer:
{answer}

Documents:
{context}
"""

        result = self.llm.generate(prompt)
        import re

        try:
            match = re.search(r"\{.*\}", result, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                return data.get("hallucination", False)
        except:
            return False
        