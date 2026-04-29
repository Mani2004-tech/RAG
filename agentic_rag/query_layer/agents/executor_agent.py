# # # import json
# # # from agentic_rag.llm.llm_client import LLMClient


# # # class ExecutorAgent:

# # #     def __init__(self):
# # #         self.llm = LLMClient()

# # #     def run(self, query, docs):

# # #         # flatten retrieved docs
# # #         context = ""

# # #         if isinstance(docs, list):

# # #             for i, d in enumerate(docs):

# # #                 if isinstance(d, dict):

# # #                     context += f"\nDocument {i+1}:\n{d.get('text', '')}\n"

# # #                 elif isinstance(d, tuple):

# # #                     context += f"\nDocument {i+1}:\n{d[0]}\n"

# # #                 else:

# # #                     context += f"\nDocument {i+1}:\n{str(d)}\n"

# # #         prompt = f"""
# # # You are an expert AI assistant answering questions using retrieved documents.

# # # Guidelines:

# # # - Answer ONLY using the provided documents.
# # # - If the documents do not contain the answer, say "Information not found in retrieved documents."
# # # - Provide a concise and factual answer.
# # # - Cite the document numbers when relevant.

# # # User Query:
# # # {query}

# # # Retrieved Documents:
# # # {context}

# # # Return the final answer.
# # # """

# # #         response = self.llm.generate(prompt)

# # #         return response

# # from agentic_rag.llm.llm_client import LLMClient
# # from agentic_rag.memory.memory_store import MemoryStore
# # from langsmith import traceable


# # class ExecutorAgent:

# #     def __init__(self):

# #         self.llm = LLMClient()
# #         self.memory = MemoryStore()

# #     @traceable(name="executor_agent")
# #     def run(self, query, docs):
# #         print("\n🔹 Executor Query:", query)
# #         print("🔹 Docs Used:", len(docs))
# #         context = ""

# #         for i,d in enumerate(docs):

# #             context += f"\nDocument {i+1}:\n{d.content}\n"

# #         prompt = f"""
# # You are an expert AI assistant answering questions using retrieved documents.

# # Rules:

# # 1. Answer ONLY using the retrieved documents.
# # 2. If answer is not present say:
# #    "Information not found in retrieved documents."
# # 3. Cite sources using [Doc1], [Doc2].
# # 4. Be concise and factual.

# # User Query:
# # {query}

# # Retrieved Documents:
# # {context}

# # Return the final answer.
# # """
# #         print("\n🔹 Context Sent To LLM:")
# #         print(context[:800])
# #         answer = self.llm.generate(prompt)

# #         if "Information not found" in answer:

# #             self.memory.store_failure(
# #                 query,
# #                 "retrieval_failure"
# #             )
# #         print("\n🔹 Final Answer:", answer)
# #         return answer

# # from agentic_rag.llm.llm_client import LLMClient
# # from agentic_rag.memory.memory_store import MemoryStore
# # from langsmith import traceable

# # class ExecutorAgent:

# #     def __init__(self):

# #         print("🧠 Executor Agent Initialized")

# #         self.llm = LLMClient()
# #         self.memory = MemoryStore()

# #     @traceable(name="executor_agent")
# #     def run(self, query, docs):

# #         print("\n==============================")
# #         print("🧠 EXECUTOR AGENT START")
# #         print("Query:", query)
# #         print("Docs received:", len(docs))
# #         print("==============================")

# #         context = ""

# #         for i, d in enumerate(docs):

# #             context += f"\nDocument {i+1}:\n{d.content}\n"

# #         past_queries = self.memory.fetch_similar_queries(query)

# #         history = ""

# #         for h in past_queries:
# #             history += str(h) + "\n"

# #         prompt = f"""
# # You are an expert AI assistant answering questions using retrieved documents.

# # Rules:

# # 1. Answer ONLY using the retrieved documents.
# # 2. If answer is not present say:
# #    "Information not found in retrieved documents."
# # 3. Be concise and factual.


# # Recent related queries:
# # {history}

# # User Query:
# # {query}

# # Documents:
# # {context}

# # Rules:

# # - Answer ONLY using documents
# # - If not found say "Information not found in retrieved documents"
# # """

# #         print("\n📤 Sending prompt to LLM")

# #         answer = self.llm.generate(prompt)

# #         print("\n📥 LLM Answer:")
# #         print(answer)

# #         if "Information not found" in answer:

# #             print("⚠ Retrieval failure stored")

# #             self.memory.store_failure(
# #                 query,
# #                 "retrieval_failure"
# #             )

# #         print("🧠 EXECUTOR END\n")

# #         return answer
# from agentic_rag.llm.llm_client import LLMClient

# from agentic_rag.memory.memory_store import MemoryStore
# from langsmith import traceable


# class ExecutorAgent:

#     def __init__(self):

#         print("🧠 Executor Agent Initialized")

#         self.llm = LLMClient()
#         self.memory = MemoryStore()

#     @traceable(name="executor_agent")
#     def run(self, query, docs, chat_history=None):

      

#         print("\n==============================")
#         print("🧠 EXECUTOR AGENT START")
#         print("Query:", query)
#         print("Docs received:", len(docs))
#         print("==============================")

#         context = ""

#         for i, d in enumerate(docs):
#             context += f"\nDocument {i+1}:\n{d.content}\n"

#         history_text = ""

#         if chat_history:
#             for h in chat_history[-5:]:
#                 role = h.get("role", "")
#                 content = h.get("content", "")
#                 history_text += f"{role}: {content}\n"

#         past_queries = self.memory.fetch_similar_queries(query)

#         memory_text = ""

#         for h in past_queries:
#             memory_text += str(h) + "\n"

#         prompt = f"""You are an expert AI assistant answering questions using retrieved documents.

# Rules:

# 1. Answer ONLY using the retrieved documents.
# 2. If answer is not present say:
#    "Information not found in retrieved documents."
# 3. Be concise and factual.


# Recent related queries:
# {history}

# User Query:
# {query}

# Documents:
# {context}

# Rules:

# - Answer ONLY using documents
# - If not found say "Information not found in retrieved documents"""

#         print("\n📤 Sending prompt to LLM")

#         answer = self.llm.generate(prompt).strip()

#         print("\n📥 LLM Answer:")
#         print(answer)

#         if "NOT_FOUND" in answer or "Information not found" in answer:
#             print("⚠ Retrieval failure detected")
       
#             self.memory.store_failure(query, "retrieval_failure")

#             return {
#                 "answer": "NOT_FOUND",
#                 "retrieval_failed": True
#             }

  

#         print("🧠 EXECUTOR END\n")

#         return {
#             "answer": answer,
#             "retrieval_failed": False
#         }

from agentic_rag.llm.llm_client import LLMClient
from agentic_rag.memory.memory_store import MemoryStore
from langsmith import traceable


class ExecutorAgent:

    def __init__(self):
        print("🧠 Executor Agent Initialized")
        self.llm = LLMClient()
        self.memory = MemoryStore()

    # ------------------------------
    # 🔹 SUMMARIZE LAST 5 CONVERSATIONS
    # ------------------------------
    def summarize_history(self, chat_history):

        if not chat_history:
            return ""

        last_msgs = chat_history[-5:]

        history_str = ""

        for h in last_msgs:
            role = h.get("role", "")
            content = h.get("content", "")
            history_str += f"{role}: {content}\n"

        prompt = f"""
Summarize the following conversation in 2-3 lines focusing on intent and context:

{history_str}

Summary:
"""

        try:
            summary = self.llm.generate(prompt).strip()
            return summary
        except Exception as e:
            print("⚠ History summarization failed:", e)
            return ""

    # ------------------------------
    # 🔹 MAIN EXECUTOR
    # ------------------------------
    @traceable(name="executor_agent")
    def run(self, query, docs, chat_history=None):

        print("\n==============================")
        print("🧠 EXECUTOR AGENT START")
        print("Query:", query)
        print("Docs received:", len(docs))
        print("==============================")

        # ------------------------------
        # BUILD CONTEXT FROM DOCS
        # ------------------------------
        context = ""

        for i, d in enumerate(docs):
            try:
                context += f"\nDocument {i+1}:\n{d.content}\n"
            except:
                context += f"\nDocument {i+1}:\n{str(d)}\n"

        print("\n📚 Context Preview:")
        print(context[:500])

        # ------------------------------
        # SUMMARIZE CHAT HISTORY
        # ------------------------------
        history_text = self.summarize_history(chat_history)

        # ------------------------------
        # FETCH MEMORY (PAST SIMILAR QUERIES)
        # ------------------------------
        past_queries = self.memory.fetch_similar_queries(query)

        memory_text = ""

        for h in past_queries:
            memory_text += str(h) + "\n"

        # ------------------------------
        # FINAL PROMPT
        # ------------------------------
        prompt = f"""
You are an expert AI assistant answering questions using retrieved documents.

Rules:
- Answer ONLY using the documents
- If answer not present say "NOT_FOUND"
- Be concise and factual
- Do NOT hallucinate

Conversation Summary:
{history_text}

Relevant Past Queries:
{memory_text}

User Query:
{query}

Documents:
{context}

Final Answer:
"""

        print("\n📤 Sending prompt to LLM...")

        # ------------------------------
        # GENERATE ANSWER
        # ------------------------------
        try:
            answer = self.llm.generate(prompt).strip()
        except Exception as e:
            print("❌ LLM Error:", e)
            return {
                "answer": "ERROR",
                "retrieval_failed": True
            }

        print("\n📥 LLM Answer:")
        print(answer)

        # ------------------------------
        # HANDLE RETRIEVAL FAILURE
        # ------------------------------
        if (
            not answer
            or "NOT_FOUND" in answer
            or "Information not found" in answer
        ):
            print("⚠ Retrieval failure detected")

            self.memory.store_failure(
                query,
                "retrieval_failure"
            )

            return {
                "answer": "NOT_FOUND",
                "retrieval_failed": True
            }

        print("🧠 EXECUTOR END\n")

        return {
            "answer": answer,
            "retrieval_failed": False
        }