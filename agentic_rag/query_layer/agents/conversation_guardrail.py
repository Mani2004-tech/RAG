
# from langsmith import traceable
# from agentic_rag.llm.llm_client import LLMClient
# import json


# class ConversationGuardrail:

#     def __init__(self):
#         self.llm = LLMClient()
#     @traceable(name="conversation_guardrail", run_type="llm")
#     def check(self, query):

#         print("\n🔹 Conversation Guardrail Input:", query)

#         prompt = f"""
# You are a conversation guardrail.

# Classify the query as either a greeting or a question that requires some knowledge.

# Return JSON:

# type:
# - conversational
# - knowledge

# Conversational queries include:
# greetings, small talk, pleasantries, chit-chat.

# Examples:
# hi,
# hello,
# how are you,
# good morning,
# good evening,
# what's up

# These should be conversational.

# Knowledge queries require factual answers.

# Query:
# {query}
# """

#         response = self.llm.generate(prompt)

#         try:
#             result = json.loads(response)
#         except:
#             result = {"type": "knowledge"}
#         print("\n🔹 Conversation Guardrail result:", result)
#         return result
from langsmith import traceable
from agentic_rag.llm.llm_client import LLMClient
import json
import re


class ConversationGuardrail:

    def __init__(self):
        self.llm = LLMClient()

        # ------------------------------
        # RULE ENGINE
        # ------------------------------
        self.patterns = {
            "conversational": [
                r"\bhi\b", r"\bhello\b", r"\bhey\b", r"\bsup\b",
                r"\bhow are you\b", r"\bhow r u\b",
                r"\bgood (morning|afternoon|evening)\b",
                r"\bthanks?\b", r"\bthank you\b",
                r"\bok\b", r"\bcool\b"
            ],
            "meta": [
                r"\bwho are you\b", r"\bwho r u\b",
                r"\bwhat can you do\b",
                r"\bintroduce yourself\b"
            ],
            "harmful": [
                r"\bkill\b", r"\bhack\b", r"\battack\b"
            ]
        }

    # ------------------------------
    # NORMALIZATION
    # ------------------------------
    def _normalize(self, query: str) -> str:
        query = query.lower().strip()

        slang_map = {
            "r u": "are you",
            "wht": "what",
            "u": "you"
        }

        for k, v in slang_map.items():
            query = query.replace(k, v)

        return query

    # ------------------------------
    # RULE CHECK
    # ------------------------------
    def _rule_check(self, query):

        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return intent

        # short queries heuristic
        if len(query.split()) <= 2:
            return "conversational"

        return None

    # ------------------------------
    # LLM CLASSIFIER
    # ------------------------------
    def _llm_classify(self, query):

        prompt = f"""
You are a STRICT intent classifier.

Classify query into:

- conversational (greetings, chit-chat)
- meta (about assistant)
- knowledge (needs factual answer)
- harmful (unsafe intent)
- unclear (ambiguous)

STRICT RULES:
- "who are you" → meta
- greetings → conversational
- unsafe → harmful
- factual → knowledge

Return ONLY JSON:
{{"intent": "..."}}

Query: {query}
"""

        response = self.llm.generate(prompt)

        try:
            return json.loads(response)
        except:
            return {"intent": "knowledge"}

    # ------------------------------
    # MAIN ENTRY
    # ------------------------------
    @traceable(name="conversation_guardrail", run_type="chain")
    def check(self, query):

        print("\n🔹 Guardrail Input:", query)

        query = self._normalize(query)

        # 1️⃣ RULE ENGINE
        rule_intent = self._rule_check(query)

        if rule_intent:
            result = {"intent": rule_intent}
            print("🔹 Rule Intent:", result)
            return result

        # 2️⃣ LLM FALLBACK
        result = self._llm_classify(query)

        print("🔹 LLM Intent:", result)

        return result