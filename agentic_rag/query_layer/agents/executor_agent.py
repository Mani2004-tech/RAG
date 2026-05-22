from langsmith import traceable

from agentic_rag.llm.llm_client import LLMClient
from agentic_rag.memory.memory_store import MemoryStore


class ExecutorAgent:

    def __init__(self):
        print("🧠 Executor Agent Initialized")
        self.llm = LLMClient()
        self.memory = MemoryStore()

    @traceable(name="executor_agent")
    def run(self, query, docs):
        print("\n==============================")
        print("🧠 EXECUTOR AGENT START")
        print("Query:", query)
        print("Docs received:", len(docs))
        print("==============================")

        context = ""
        for i, d in enumerate(docs):
            context += f"\nDocument {i+1}:\n{d.content}\n"

        past_queries = self.memory.fetch_similar_queries(query)
        history = ""
        for h in past_queries:
            history += str(h) + "\n"

        prompt = f"""
You are an expert AI assistant answering questions using retrieved documents.

Rules:

1. Answer ONLY using the retrieved documents.
2. If answer is not present say:
   "Information not found in retrieved documents."
3. Be concise and factual.


Recent related queries:
{history}

User Query:
{query}

Documents:
{context}

Rules:

- Answer ONLY using documents
- If not found say "Information not found in retrieved documents"
"""

        print("\n📤 Sending prompt to LLM")
        answer = self.llm.generate(prompt)

        print("\n📥 LLM Answer:")
        print(answer)

        if "Information not found" in answer:
            print("⚠ Retrieval failure stored")
            self.memory.store_failure(query, "retrieval_failure")

        print("🧠 EXECUTOR END\n")
        return answer
