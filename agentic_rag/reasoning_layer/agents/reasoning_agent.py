
from langsmith import traceable
from agentic_rag.memory.memory_store import MemoryStore
from agentic_rag.llm.llm_client import LLMClient
import json


class ReasoningAgent:

    def __init__(self):

        print("🧠 Reasoning Agent Initialized")

        self.llm = LLMClient()
        self.memory = MemoryStore()

    @traceable(name="reasoning_agent")
    def evaluate(self, query, answer, docs):

        # ✅ HARD FAILURE CHECK (CRITICAL FIX)
        if answer == "NOT_FOUND":

            print("❌ Answer not found → forcing retry")

            return {
                "complete": False,
                "needs_retrieval": True,
                "confidence": 0.0
            }

        # format docs
        context = ""
        for i, d in enumerate(docs[:5]):
            context += f"\nDoc{i+1}: {d.content[:300]}\n"

        prompt = f"""
Evaluate answer quality.

Query:
{query}

Answer:
{answer}

Documents:
{context}

Return JSON:

complete: true/false
needs_retrieval: true/false
confidence: 0.0-1.0

Rules:
- If answer is weak → complete=false
- If docs irrelevant → needs_retrieval=true
- If answer missing info → complete=false
"""

        response = self.llm.generate(prompt)

        try:
            result = json.loads(response)
            result["confidence"] = float(result.get("confidence", 0.5))
        except:
            result = {
                "complete": False,
                "needs_retrieval": True,
                "confidence": 0.3
            }

        # safety override
        if not result.get("complete"):
            result["needs_retrieval"] = True

        print("\n🔹 Reasoning Result:", result)

        return result