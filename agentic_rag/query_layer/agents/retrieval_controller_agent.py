import json
import re

from langsmith import traceable

from agentic_rag.llm.llm_client import LLMClient


class RetrievalControllerAgent:

    def __init__(self):
        self.llm = LLMClient()

    @traceable(name="retrieval_controller_agent")
    def run(self, query, index, planner_filters=None):
        print("\n🔹 Retrieval Controller Node")
        print("Query:", query)
        print("Selected Index:", index)
        print("Planner Metadata Filters:", planner_filters)

        if planner_filters is None:
            planner_filters = {}

        prompt = f"""
You are a retrieval controller for an Agentic RAG system.

Decide optimal retrieval parameters.

Return JSON with fields:

tool: retrieval index to use
top_k: number of documents to retrieve
metadata_filter: metadata filtering dictionary

Rules:

- Preserve planner metadata filters if they exist
- If query is broad → increase top_k
- If query is specific → reduce top_k
- If query references time → use temporal filtering
- If query mentions author/domain → use metadata filters

Query:
{query}

Selected Index:
{index}

Planner Metadata Filters:
{planner_filters}

Return JSON only.
"""

        response = self.llm.generate(prompt)
        print("LLM Raw Response:", response)

        try:
            cleaned = re.sub(r"```json|```", "", response).strip()
            params = json.loads(cleaned)
        except Exception as e:
            print("⚠ Retrieval Controller JSON parsing failed:", e)
            params = {
                "tool": index,
                "top_k": 5,
                "metadata_filter": planner_filters,
            }

        if "tool" not in params:
            params["tool"] = index

        if "top_k" not in params:
            params["top_k"] = 5

        if "metadata_filter" not in params or not params["metadata_filter"]:
            params["metadata_filter"] = planner_filters

        print("🔹 Retrieval Parameters Decision:", params)
        return params
