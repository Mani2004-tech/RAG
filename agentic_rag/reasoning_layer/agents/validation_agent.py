
from langsmith import traceable
from agentic_rag.llm.llm_client import LLMClient
import json


class ValidationAgent:

    def __init__(self):

        print("🔍 Validation Agent Initialized")

        self.llm = LLMClient()

    @traceable(name="validation_agent")
    def validate(self, query, answer, docs):

        # ❌ Reject NOT_FOUND immediately
        if answer == "NOT_FOUND":
            print("❌ Validation failed: NOT_FOUND")
            return False

        context = ""

        for i, d in enumerate(docs[:5]):
            context += f"\nDoc{i+1}: {d.content[:300]}"

        prompt = f"""
Check if the answer is supported.

Query:
{query}

Answer:
{answer}

Documents:
{context}

Return JSON:
supported:true/false
"""

        result = self.llm.generate(prompt)

        print("\n🔹 Validation Result:", result)

        try:
            parsed = json.loads(result)
            return parsed.get("supported", False)
        except:
            return False