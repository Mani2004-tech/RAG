from langsmith import traceable

from agentic_rag.llm.llm_client import LLMClient


class ValidationAgent:

    def __init__(self):
        print("🔍 Validation Agent Initialized")
        self.llm = LLMClient()

    @traceable(name="validation_agent")
    def validate(self, query, answer, docs):
        context = ""
        for i, d in enumerate(docs[:5]):
            context += f"\nDoc{i+1}: {d.content[:300]}"

        prompt = f"""
Check if the answer is supported by the retrieved documents.

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
        return "true" in result.lower()
