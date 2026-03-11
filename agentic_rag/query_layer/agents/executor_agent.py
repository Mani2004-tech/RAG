# # import json
# # from agentic_rag.llm.llm_client import LLMClient


# # class ExecutorAgent:

# #     def __init__(self):
# #         self.llm = LLMClient()

# #     def run(self, query, docs):

# #         # flatten retrieved docs
# #         context = ""

# #         if isinstance(docs, list):

# #             for i, d in enumerate(docs):

# #                 if isinstance(d, dict):

# #                     context += f"\nDocument {i+1}:\n{d.get('text', '')}\n"

# #                 elif isinstance(d, tuple):

# #                     context += f"\nDocument {i+1}:\n{d[0]}\n"

# #                 else:

# #                     context += f"\nDocument {i+1}:\n{str(d)}\n"

# #         prompt = f"""
# # You are an expert AI assistant answering questions using retrieved documents.

# # Guidelines:

# # - Answer ONLY using the provided documents.
# # - If the documents do not contain the answer, say "Information not found in retrieved documents."
# # - Provide a concise and factual answer.
# # - Cite the document numbers when relevant.

# # User Query:
# # {query}

# # Retrieved Documents:
# # {context}

# # Return the final answer.
# # """

# #         response = self.llm.generate(prompt)

# #         return response

# from agentic_rag.llm.llm_client import LLMClient
# from agentic_rag.memory.memory_store import MemoryStore
# from langsmith import traceable


# class ExecutorAgent:

#     def __init__(self):

#         self.llm = LLMClient()
#         self.memory = MemoryStore()

#     @traceable(name="executor_agent")
#     def run(self, query, docs):
#         print("\n🔹 Executor Query:", query)
#         print("🔹 Docs Used:", len(docs))
#         context = ""

#         for i,d in enumerate(docs):

#             context += f"\nDocument {i+1}:\n{d.content}\n"

#         prompt = f"""
# You are an expert AI assistant answering questions using retrieved documents.

# Rules:

# 1. Answer ONLY using the retrieved documents.
# 2. If answer is not present say:
#    "Information not found in retrieved documents."
# 3. Cite sources using [Doc1], [Doc2].
# 4. Be concise and factual.

# User Query:
# {query}

# Retrieved Documents:
# {context}

# Return the final answer.
# """
#         print("\n🔹 Context Sent To LLM:")
#         print(context[:800])
#         answer = self.llm.generate(prompt)

#         if "Information not found" in answer:

#             self.memory.store_failure(
#                 query,
#                 "retrieval_failure"
#             )
#         print("\n🔹 Final Answer:", answer)
#         return answer

from agentic_rag.llm.llm_client import LLMClient
from agentic_rag.memory.memory_store import MemoryStore
from langsmith import traceable

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

            self.memory.store_failure(
                query,
                "retrieval_failure"
            )

        print("🧠 EXECUTOR END\n")

        return answer