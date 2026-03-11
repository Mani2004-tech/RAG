import json
from agentic_rag.llm.llm_client import LLMClient


class MemoryNode:

    def __init__(self):
        self.llm = LLMClient()

    def run(self, state):

        query = state["query"]
        history = state.get("chat_history", [])

        history_text = ""

        for h in history[-10:]:
            history_text += f'{h["role"]}: {h["content"]}\n'

        prompt = f"""
You are a routing agent.

Decide if the user query should be answered from conversation history.

Return JSON:

use_memory: true or false
answer: answer if possible else ""

Query:
{query}

Conversation History:
{history_text}
"""

        response = self.llm.generate(prompt)

        try:
            result = json.loads(response)
        except:
            result = {"use_memory": False, "answer": ""}

        if result["use_memory"]:
            print("\n🔹 Memory Node Answer:", result["answer"])

            state["answer"] = result["answer"]
            state["skip_retrieval"] = True

        return state