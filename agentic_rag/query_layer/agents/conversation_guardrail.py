# from agentic_rag.llm.llm_client import LLMClient
# import json


# class ConversationGuardrail:

#     def __init__(self):
#         self.llm = LLMClient()

#     def check(self, query):

#         prompt = f"""
# Classify the query.

# Return JSON:

# type:
# - conversational
# - knowledge

# Examples:
# hi
# hello
# how are you
# good morning
# what's up

# These are conversational.

# Query:
# {query}
# """

#         result = self.llm.generate(prompt)

#         try:
#             data = json.loads(result)
#         except:
#             data = {"type": "knowledge"}

#         return data

from agentic_rag.llm.llm_client import LLMClient
import json


class ConversationGuardrail:

    def __init__(self):
        self.llm = LLMClient()

    def check(self, query):

        prompt = f"""
You are a query classifier for an AI system.

Classify the user query into ONE of the following types:

1. conversational
   greetings, chit-chat, small talk

2. knowledge
   questions requiring information retrieval

Return STRICT JSON only.

Example outputs:

{{"type":"conversational"}}

{{"type":"knowledge"}}

User Query:
{query}
"""

        result = self.llm.generate(prompt)

        print("🔹 Guardrail LLM Raw Response:", result)

        try:
            data = json.loads(result)

            if "type" not in data:
                raise ValueError("Missing type")

        except Exception:
            print("⚠ Guardrail JSON parse failed")

            # safer fallback
            data = {"type": "knowledge"}

        return data