from langsmith import traceable
from agentic_rag.memory.memory_store import MemoryStore
import json
from agentic_rag.llm.llm_client import LLMClient


class ReasoningAgent:

    def __init__(self):

        self.llm = LLMClient()
        self.memory = MemoryStore()

    @traceable(name="reasoning_agent")
    def evaluate(self, query, answer, docs):

        prompt = f"""
Evaluate answer.

Query:
{query}

Answer:
{answer}

Documents:
{docs}


Return JSON:
complete
needs_retrieval
confidence
"""

        response = self.llm.generate(prompt)

        try:
            result = json.loads(response)
        except:
            result = {"complete":True,"needs_retrieval":False,"confidence":0.7}

        if result["confidence"] < 0.6:

            self.memory.store_failure(
                query,
                "low_confidence_answer"
            )
        print("\n🔹 Reasoning Result:", result)
        return result