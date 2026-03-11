# import json
# from agentic_rag.llm.llm_client import LLMClient


# class PlannerAgent:

#     def __init__(self):
#         self.llm = LLMClient()

#     def run(self, query):

#         prompt = f"""
# You are a query analysis planner for a Retrieval Augmented Generation system.

# Analyze the user query and return structured JSON.

# Fields:

# intent:
# - search
# - explanation
# - comparison
# - definition
# - summarization
# - reasoning

# domain:
# - finance
# - legal
# - medical
# - technical
# - research
# - general

# time_sensitive:
# true if query depends on recent or time-based information

# query_complexity:
# - simple
# - multi-hop
# - analytical

# retrieval_strategy:
# choose best retrieval approach

# - vector
# - bm25
# - hybrid
# - parent_child
# - temporal

# metadata_filters:
# suggest metadata filters if useful
# (example: year, author, domain)

# User Query:
# {query}

# Return JSON only.
# """

#         response = self.llm.generate(prompt)

#         try:

#             result = json.loads(response)

#         except Exception:

#             # fallback if model returns non-json
#             result = {
#                 "intent": "search",
#                 "domain": "general",
#                 "time_sensitive": False,
#                 "query_complexity": "simple",
#                 "retrieval_strategy": "vector",
#                 "metadata_filters": {}
#             }

#         return result

import json
from agentic_rag.llm.llm_client import LLMClient
from agentic_rag.memory.memory_store import MemoryStore
from langsmith import traceable


class PlannerAgent:

    def __init__(self):

        self.llm = LLMClient()
        self.memory = MemoryStore()

    @traceable(name="planner_agent")
    def run(self, query):

        past = self.memory.fetch_similar_queries(query)
        print("\n🔹 Planner Input Query:", query)
        prompt = f"""
You are an expert query planning agent for a Retrieval Augmented Generation system.

Past similar queries and decisions:
{past}

Analyze the user query and return structured JSON.

Fields:

intent:
search | explanation | comparison | definition | summarization | reasoning

domain:
finance | legal | medical | technical | research | general

time_sensitive:
true if query depends on recent information

query_complexity:
simple | multi-hop | analytical

retrieval_strategy:
Choose based on rules:

vector
- conceptual or semantic questions
- explanations
- definitions

bm25
- exact keywords
- abbreviations
- short factual queries

hybrid
- mix of semantic + keyword search

parent_child
- long documents (books, large PDFs)

temporal
- latest news or recent information

summary_tree
- summarizing long documents

knowledge_graph
- entity relationships


metadata_filters:

Extract metadata if present in the query.

Possible metadata fields:

year
author
domain
location
topic
keywords

IMPORTANT:
Always extract important keywords from the query and add them to:

keywords: [list of keywords]

Example:

Query: "latest AI research papers 2024"

metadata_filters:
{{
"year": "2024",
"keywords": ["AI", "research"]
}}

Query: "what does MTF stand for"

metadata_filters:
{{
"keywords": ["MTF"]
}}

User Query:
{query}

Return JSON only.
"""

        response = self.llm.generate(prompt)

        try:
            plan = json.loads(response)
        except:
            plan = {
                "intent":"search",
                "domain":"general",
                "retrieval_strategy":"hybrid",
                "metadata_filters":{}
            }
        print("🔹 Planner Decision:", plan)
        self.memory.store_query(query, plan)

        return plan