# from agentic_rag.llm.llm_client import LLMClient
# from langsmith import traceable
# import json


# class RetrievalControllerAgent:

#     def __init__(self):
#         self.llm = LLMClient()

#     @traceable(name="retrieval_controller_agent")
#     def run(self, query, index):

#         print("\n🔹 Retrieval Controller Node")
#         print("Query:", query)
#         print("Selected Index:", index)

#         prompt = f"""
# You are a retrieval controller for an Agentic RAG system.

# Decide optimal retrieval parameters.

# Return JSON with fields:

# tool: retrieval index to use
# top_k: number of documents to retrieve
# metadata_filter: metadata filtering dictionary

# Rules:

# - If query is broad → increase top_k
# - If query is specific → reduce top_k
# - If query references time → use temporal filtering
# - If query mentions author/domain → use metadata filters

# Query:
# {query}

# Selected Index:
# {index}

# Return JSON only.
# """

#         try:

#             response = self.llm.generate(prompt)

#             print("LLM Raw Response:", response)

#             params = json.loads(response)

#         except Exception as e:

#             print("⚠ Retrieval Controller JSON parsing failed:", e)

#             params = {
#                 "tool": index,
#                 "top_k": 5,
#                 "metadata_filter": {}
#             }

#         # ---- Safety corrections ----

#         if "tool" not in params:
#             params["tool"] = index

#         if "top_k" not in params:
#             params["top_k"] = 5

#         if "metadata_filter" not in params:
#             params["metadata_filter"] = {}

#         # ensure top_k valid
#         if not isinstance(params["top_k"], int):
#             params["top_k"] = 5

#         if params["top_k"] > 20:
#             params["top_k"] = 20

#         if params["top_k"] < 3:
#             params["top_k"] = 3

#         print("🔹 Retrieval Parameters Decision:", params)

#         return params




# Proper Fix: Clean the LLM Output Before Parsing


from agentic_rag.llm.llm_client import LLMClient
from langsmith import traceable
import json
import re


class RetrievalControllerAgent:

    def __init__(self):
        self.llm = LLMClient()

    @traceable(name="retrieval_controller_agent")
    def run(self, query, index):

        print("\n🔹 Retrieval Controller Node")
        print("Query:", query)
        print("Selected Index:", index)

        prompt = f"""
You are a retrieval controller for an Agentic RAG system.

Decide optimal retrieval parameters.

Return JSON with fields:

tool: retrieval index to use
top_k: number of documents to retrieve
metadata_filter: metadata filtering dictionary

Rules:

- If query is broad → increase top_k
- If query is specific → reduce top_k
- If query references time → use temporal filtering
- If query mentions author/domain → use metadata filters

Query:
{query}

Selected Index:
{index}

Return JSON only.
"""

        response = self.llm.generate(prompt)

        print("LLM Raw Response:", response)

        try:
            # Remove markdown code blocks if present
            cleaned = re.sub(r"```json|```", "", response).strip()

            params = json.loads(cleaned)

        except Exception as e:

            print("⚠ Retrieval Controller JSON parsing failed:", e)

            params = {
                "tool": index,
                "top_k": 5,
                "metadata_filter": {}
            }

        # Safety defaults
        if "tool" not in params:
            params["tool"] = index

        if "top_k" not in params:
            params["top_k"] = 5

        if "metadata_filter" not in params:
            params["metadata_filter"] = {}

        print("🔹 Retrieval Parameters Decision:", params)

        return params