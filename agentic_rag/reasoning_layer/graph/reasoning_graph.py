from langgraph.graph import StateGraph, END

from agentic_rag.reasoning_layer.agents.reasoning_agent import ReasoningAgent
from agentic_rag.reasoning_layer.agents.validation_agent import ValidationAgent
from agentic_rag.reasoning_layer.agents.retry_decision_agent import RetryDecisionAgent

from agentic_rag.guardrails.hallucination_checker import HallucinationChecker
from agentic_rag.guardrails.citation_enforcer import CitationEnforcer


reasoner = ReasoningAgent()
validator = ValidationAgent()
retry_agent = RetryDecisionAgent()

hallucination = HallucinationChecker()
citation = CitationEnforcer()


def reasoning_node(state):

    result = reasoner.evaluate(
        state["query"],
        state["answer"],
        state["docs"]
    )

    state["reasoning"] = result

    return state


def validation_node(state):

    valid = validator.validate(
        state["query"],
        state["answer"],
        state["docs"]
    )

    state["valid"] = valid

    return state


def guardrail_node(state):

    if hallucination.check(
        state["query"],
        state["answer"],
        state["docs"]
    ):
        state["retry"] = True
        return state

    state["answer"] = citation.enforce(state["answer"])

    return state


def retry_node(state):

    retry = retry_agent.decide(state["reasoning"])

    state["retry"] = retry

    return state


builder = StateGraph(dict)

builder.add_node("reason", reasoning_node)
builder.add_node("validate", validation_node)
builder.add_node("guardrails", guardrail_node)
builder.add_node("retry", retry_node)

builder.set_entry_point("reason")

builder.add_edge("reason", "validate")
builder.add_edge("validate", "guardrails")
builder.add_edge("guardrails", "retry")

builder.add_conditional_edges(
    "retry",
    lambda s: END
)

reasoning_graph = builder.compile()

from IPython.display import Image, display
import os

png1 = reasoning_graph.get_graph().draw_mermaid_png()

with open("reasoning_graph.png", "wb") as f:
    f.write(png1)

os.startfile("reasoning_graph.png")   # Windows