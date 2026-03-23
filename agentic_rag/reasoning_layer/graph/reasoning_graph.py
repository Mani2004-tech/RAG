# from langgraph.graph import StateGraph, END

# from agentic_rag.reasoning_layer.agents.reasoning_agent import ReasoningAgent
# from agentic_rag.reasoning_layer.agents.validation_agent import ValidationAgent
# from agentic_rag.reasoning_layer.agents.retry_decision_agent import RetryDecisionAgent

# from agentic_rag.guardrails.hallucination_checker import HallucinationChecker
# from agentic_rag.guardrails.citation_enforcer import CitationEnforcer


# reasoner = ReasoningAgent()
# validator = ValidationAgent()
# retry_agent = RetryDecisionAgent()

# hallucination = HallucinationChecker()
# citation = CitationEnforcer()


# def reasoning_node(state):

#     result = reasoner.evaluate(
#         state["query"],
#         state["answer"],
#         state["docs"]
#     )

#     state["reasoning"] = result

#     return state


# def validation_node(state):

#     valid = validator.validate(
#         state["query"],
#         state["answer"],
#         state["docs"]
#     )

#     state["valid"] = valid

#     return state


# def guardrail_node(state):

#     if hallucination.check(
#         state["query"],
#         state["answer"],
#         state["docs"]
#     ):
#         state["retry"] = True
#         return state

#     state["answer"] = citation.enforce(state["answer"])

#     return state


# def retry_node(state):

#     retry = retry_agent.decide(state["reasoning"])

#     state["retry"] = retry

#     return state


# builder = StateGraph(dict)

# builder.add_node("reason", reasoning_node)
# builder.add_node("validate", validation_node)
# builder.add_node("guardrails", guardrail_node)
# builder.add_node("retry", retry_node)

# builder.set_entry_point("reason")

# builder.add_edge("reason", "validate")
# builder.add_edge("validate", "guardrails")
# builder.add_edge("guardrails", "retry")

# builder.add_conditional_edges(
#     "retry",
#     lambda s: END
# )

# reasoning_graph = builder.compile()

from langsmith import traceable
from agentic_rag.llm.llm_client import LLMClient


class ValidationAgent:


    def __init__(self):

        print("🔍 Validation Agent Initialized")

        self.llm = LLMClient()


    @traceable(name="validation_agent")
    def validate(self, query, answer, docs):

        context = ""

        for i, d in enumerate(docs[:5]):

            context += f"\nDoc{i+1}: {d.content[:300]}"


        prompt = f"""
Check if answer is supported by documents.

Query:
{query}

Answer:
{answer}

Documents:
{context}

Return JSON:

supported:true/false
"""


        result = self.llm.generate(prompt)

        print("\n🔹 Validation:", result)

        return "true" in result.lower()