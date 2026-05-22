import json

from langsmith import traceable

from agentic_rag.llm.llm_client import LLMClient
from agentic_rag.memory.memory_store import MemoryStore


class ReasoningAgent:

    def __init__(self):
        print("🧠 Reasoning Agent Initialized")
        self.llm = LLMClient()
        self.memory = MemoryStore()

    @traceable(name="reasoning_agent")
    def evaluate(self, query, answer, docs):
        context = ""
        for i, d in enumerate(docs[:5]):
            context += f"\nDoc{i+1}: {d.content[:400]}\n"

        prompt = f"""
Evaluate the answer quality for a RAG system.

Query:
{query}

Answer:
{answer}

Retrieved Documents:
{context}

Return JSON:

complete: true/false
needs_retrieval: true/false
confidence: 0.0-1.0

Rules:

complete = true if answer fully answers query
needs_retrieval = true if documents are irrelevant or missing
confidence = reliability score
"""

        response = self.llm.generate(prompt)

        try:
            result = json.loads(response)
            result["confidence"] = float(result.get("confidence", 0.7))
        except Exception:
            result = {
                "complete": True,
                "needs_retrieval": False,
                "confidence": 0.7,
            }

        if result["confidence"] < 0.6:
            self.memory.store_failure(query, "low_confidence_answer")

        print("\n🔹 Reasoning Result:", result)
        return result
