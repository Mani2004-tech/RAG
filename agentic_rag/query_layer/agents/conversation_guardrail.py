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

        print("\n🔹 Conversation Guardrail Input:", query)

        prompt = f"""
You are a conversation guardrail.

Classify the query as either a greeting or a question that requires some knowledge.

Return JSON:

type:
- conversational
- knowledge

Conversational queries include:
greetings, small talk, pleasantries, chit-chat.

Examples:
hi
hello
how are you
good morning
good evening
what's up

These should be conversational.

Knowledge queries require factual answers.

Query:
{query}
"""

        response = self.llm.generate(prompt)

        try:
            result = json.loads(response)
        except:
            result = {"type": "knowledge"}
        print("\n🔹 Conversation Guardrail result:", result)
        return result