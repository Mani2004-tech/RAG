from agentic_rag.llm.llm_client import LLMClient


class CitationEnforcer:

    def __init__(self):

        self.llm = LLMClient()

    def enforce(self, answer):

        prompt = f"""
Rewrite the answer to include citations.

Rules:
- Every factual statement MUST have citation [DocX]
- Use only provided docs (assume they exist)
- Do not hallucinate

Format:
Sentence [Doc1]

Answer:
{answer}
"""

        return self.llm.generate(prompt)