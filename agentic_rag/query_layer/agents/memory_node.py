
# from langsmith import traceable
# from agentic_rag.langfuse_client import langfuse
# from agentic_rag.llm.llm_client import LLMClient
# import json


# class MemoryNode:

#     def __init__(self):
#         self.llm = LLMClient()
#     @traceable(name="memory_node", run_type="chain")
#     def run(self, state):
#         span = langfuse.trace(name="memory_node", input=state["query"])
#         query = state["query"]
#         history = state.get("chat_history", [])

#         # build session-only history
#         history_text = ""

#         for h in history[-5:]:
#             role = h.get("role", "")
#             content = h.get("content", "")
#             history_text += f"{role}: {content}\n"

#         prompt = f"""
# You are a memory router for a conversational AI.

# Decide if the user's question can be answered using the conversation history.

# Return JSON:

# use_memory: true or false
# answer: answer if possible else ""

# Rules:

# use_memory = true only if:
# - query refers to earlier messages
# - query asks clarification
# - query references previous answer

# use_memory = false if:
# - query requires external knowledge
# - query requires document retrieval

# User Query:
# {query}

# Conversation History:
# {history_text}
# """

#         response = self.llm.generate(prompt)

#         try:
#             result = json.loads(response)
#         except:
#             result = {"use_memory": False, "answer": ""}

#         if result["use_memory"]:

#             state["answer"] = result["answer"]
#             state["skip_retrieval"] = True

#             print("\n🔹 Memory Router Answer:", result["answer"])

#         else:

#             state["skip_retrieval"] = False
#         span.end(output=state)
#         return state
from langsmith import traceable

from agentic_rag.llm.llm_client import LLMClient
import json


class MemoryNode:

    def __init__(self):
        self.llm = LLMClient()

    @traceable(name="memory_node", run_type="chain")
    def run(self, state):

        # ✅ SUPPORT HIERARCHICAL TRACE
        

        query = state["query"]
        history = state.get("chat_history", [])

        history_text = ""

        for h in history[-5:]:
            role = h.get("role", "")
            content = h.get("content", "")
            history_text += f"{role}: {content}\n"

        prompt = f"""
You are a memory router for a conversational AI.

Decide if the user's question can be answered using the conversation history.

Return JSON:

use_memory: true or false
answer: answer if possible else ""

Rules:

use_memory = true only if:
- query refers to earlier messages
- query asks clarification
- query references previous answer

use_memory = false if:
- query requires external knowledge
- query requires document retrieval

User Query:
{query}

Conversation History:
{history_text}
"""

        response = self.llm.generate(prompt)

        try:
            result = json.loads(response)
        except:
            result = {"use_memory": False, "answer": ""}

        # if result["use_memory"]:
        #     state["answer"] = result["answer"]
        #     state["skip_retrieval"] = True
        #     print("\n🔹 Memory Router Answer:", result["answer"])
        # else:
        #     state["skip_retrieval"] = False
        if result.get("use_memory") and result.get("answer"):
            state["answer"] = result["answer"]
            state["skip_retrieval"] = True
        else:
            state["skip_retrieval"] = False
        

       
        return state