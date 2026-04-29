
# from langsmith import traceable
# from agentic_rag.memory.memory_store import MemoryStore
# from agentic_rag.llm.llm_client import LLMClient
# import json


# class ReasoningAgent:

#     def __init__(self):

#         print("🧠 Reasoning Agent Initialized")

#         self.llm = LLMClient()
#         self.memory = MemoryStore()

#     @traceable(name="reasoning_agent")
#     def evaluate(self, query, answer, docs):

#         # ✅ HARD FAILURE CHECK (CRITICAL FIX)
#         if answer == "NOT_FOUND":

#             print("❌ Answer not found → forcing retry")

#             return {
#                 "complete": False,
#                 "needs_retrieval": True,
#                 "confidence": 0.0
#             }

#         # format docs
#         context = ""
#         for i, d in enumerate(docs[:5]):
#             context += f"\nDoc{i+1}: {d.content[:300]}\n"

#         prompt = f"""
# Evaluate answer quality.

# Query:
# {query}

# Answer:
# {answer}

# Documents:
# {context}

# Return JSON:

# complete: true/false
# needs_retrieval: true/false
# confidence: 0.0-1.0

# Rules:
# - If answer is weak → complete=false
# - If docs irrelevant → needs_retrieval=true
# - If answer missing info → complete=false
# """

#         response = self.llm.generate(prompt)

#         try:
#             result = json.loads(response)
#             result["confidence"] = float(result.get("confidence", 0.5))
#         except:
#             result = {
#                 "complete": False,
#                 "needs_retrieval": True,
#                 "confidence": 0.3
#             }

#         # safety override
#         if not result.get("complete"):
#             result["needs_retrieval"] = True

#         print("\n🔹 Reasoning Result:", result)

#         return result
from langsmith import traceable
from agentic_rag.memory.memory_store import MemoryStore
from agentic_rag.llm.llm_client import LLMClient
import json
import re



class ReasoningAgent:

    def __init__(self):

        print("🧠 Reasoning Agent Initialized")

        self.llm = LLMClient()
        self.memory = MemoryStore()

    @traceable(name="reasoning_agent")
    def evaluate(self, query, answer, docs, eval_scores=None):
       
        # ✅ HARD FAILURE CHECK (CRITICAL FIX)
        if answer == "NOT_FOUND":

            print("❌ Answer not found → forcing retry")

            return {
                "complete": False,
                "needs_retrieval": True,
                "confidence": 0.0
            }
        # ------------------------------
        # 🔥 INSERT HERE (YOUR BLOCK)
        # ------------------------------
        if eval_scores:

            print("\n📊 Evaluation Scores:", eval_scores)

            if eval_scores.get("answer_relevancy", 0) < 0.5:
                return {"complete": False, "needs_retrieval": True, "confidence": 0.3}

            if eval_scores.get("faithfulness", 0) < 0.5:
                return {"complete": False, "needs_retrieval": True, "confidence": 0.3}

            if eval_scores.get("contextual_recall", 0) < 0.4:
                return {"complete": False, "needs_retrieval": True, "confidence": 0.3}

            if eval_scores.get("conversation_completeness", 0) < 0.5:
                return {"complete": False, "needs_retrieval": True, "confidence": 0.3}

            # 🔒 SAFETY FAIL
            if eval_scores.get("toxicity", 0) > 0.5:
                return {"complete": False, "needs_retrieval": False, "confidence": 0.2}

            if eval_scores.get("pii_leakage", 0) > 0.3:
                return {"complete": False, "needs_retrieval": False, "confidence": 0.2}

            if eval_scores.get("bias", 0) > 0.6:
                return {"complete": False, "needs_retrieval": False, "confidence": 0.2}

            if eval_scores.get("role_adherence", 0) < 0.5:
                return {"complete": False, "needs_retrieval": False, "confidence": 0.3}

            # ✅ PASS
            return {
                "complete": True,
                "needs_retrieval": False,
                "confidence": 0.9
            }


        # ------------------------------
        # FORMAT DOCS
        # ------------------------------
        context = ""
        for i, d in enumerate(docs[:5]):
            context += f"\nDoc{i+1}: {d.content[:300]}\n"

        # ------------------------------
        # ✅ STRONG PROMPT (STRICT JSON)
        # ------------------------------
        prompt = f"""
You are a STRICT evaluation system.

Return ONLY valid JSON. No explanation.

Format EXACTLY like:

{{
  "complete": true,
  "needs_retrieval": false,
  "confidence": 0.85
}}

Rules:
- complete = true only if answer fully answers query
- needs_retrieval = true if docs insufficient
- confidence between 0 and 1

Query:
{query}

Answer:
{answer}

Documents:
{context}
"""

        # ------------------------------
        # CALL LLM
        # ------------------------------
        response = self.llm.generate(prompt)

        print("\n🔹 Raw Reasoning LLM Output:", response)

        # ------------------------------
        # ✅ ROBUST JSON PARSING FIX
        # ------------------------------
        try:
            # 1️⃣ Remove markdown blocks (```json ``` etc)
            cleaned = re.sub(r"```json|```", "", response).strip()

            # 2️⃣ Extract JSON object if extra text exists
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if match:
                cleaned = match.group(0)

            # 3️⃣ Parse JSON
            result = json.loads(cleaned)

            # 4️⃣ Ensure proper types
            result["confidence"] = float(result.get("confidence", 0.5))
            result["complete"] = bool(result.get("complete", False))
            result["needs_retrieval"] = bool(result.get("needs_retrieval", True))

        except Exception as e:

            print("⚠ Reasoning JSON parse failed:", e)

            result = {
                "complete": False,
                "needs_retrieval": True,
                "confidence": 0.3
            }

        # ------------------------------
        # SAFETY OVERRIDE (UNCHANGED LOGIC)
        # ------------------------------
        if not result.get("complete"):
            result["needs_retrieval"] = True

        print("\n🔹 Reasoning Result:", result)
      
        return result