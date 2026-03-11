from agentic_rag.llm.llm_client import LLMClient


class CitationEnforcer:

    def __init__(self):

        self.llm = LLMClient()

    def enforce(self, answer):

        prompt = f"""
Ensure answer includes citations like [Doc1], [Doc2].

Rewrite if needed.

Answer:
{answer}
"""

        return self.llm.generate(prompt)