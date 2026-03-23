# from langsmith import traceable
# from agentic_rag.memory.memory_store import MemoryStore
# import json
# from agentic_rag.llm.llm_client import LLMClient


# class ReasoningAgent:

#     def __init__(self):

#         self.llm = LLMClient()
#         self.memory = MemoryStore()

#     @traceable(name="reasoning_agent")
#     def evaluate(self, query, answer, docs):

#         prompt = f"""
# Evaluate answer.

# Query:
# {query}

# Answer:
# {answer}

# Documents:
# {docs}


# Return JSON:
# complete
# needs_retrieval
# confidence
# """

#         response = self.llm.generate(prompt)

#         try:
#             result = json.loads(response)
#         except:
#             result = {"complete":True,"needs_retrieval":False,"confidence":0.7}

#         if result["confidence"] < 0.6:

#             self.memory.store_failure(
#                 query,
#                 "low_confidence_answer"
#             )
#         print("\n🔹 Reasoning Result:", result)
#         return result
from langsmith import traceable
from agentic_rag.memory.memory_store import MemoryStore
from agentic_rag.llm.llm_client import LLMClient
import json


class ReasoningAgent:

    def __init__(self):

        print("🧠 Reasoning Agent Initialized")

        self.llm = LLMClient()

        try:
            self.memory = MemoryStore()
        except:
            print("⚠️ Memory Disabled")
            self.memory = None


    @traceable(name="reasoning_agent")
    def evaluate(self, query, answer, docs):

        context = ""

        for i, d in enumerate(docs[:5]):
            context += f"\nDoc{i+1}: {d.content[:400]}\n"


        prompt = f"""
Evaluate answer quality for RAG system.

Query:
{query}

Answer:
{answer}

Documents:
{context}

Return JSON:

complete:true/false
needs_retrieval:true/false
confidence:0.0-1.0
"""


        response = self.llm.generate(prompt)

        try:

            result = json.loads(response)

            result["confidence"] = float(
                result.get("confidence", 0.7)
            )

        except:

            result = {

                "complete": True,

                "needs_retrieval": False,

                "confidence": 0.7

            }


        if self.memory:

            if result["confidence"] < 0.6:

                self.memory.store_failure(
                    query,
                    "low_confidence_answer"
                )


        print("\n🔹 Reasoning Result:", result)

        return result