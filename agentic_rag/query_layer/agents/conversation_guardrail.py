from agentic_rag.llm.llm_client import LLMClient
import json


class ConversationGuardrail:

    def __init__(self):
        self.llm = LLMClient()

    def check(self, query):

        prompt = f"""
Classify the query.

Return JSON:

type:
- conversational
- knowledge

Examples:
hi
hello
how are you
good morning
what's up

These are conversational.

Query:
{query}
"""

        result = self.llm.generate(prompt)

        try:
            data = json.loads(result)
        except:
            data = {"type": "knowledge"}

        return data