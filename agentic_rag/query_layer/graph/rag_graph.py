import os

from langgraph.graph import END, StateGraph
from langsmith import traceable

from agentic_rag.query_layer.agents.conversation_guardrail import ConversationGuardrail
from agentic_rag.query_layer.agents.executor_agent import ExecutorAgent
from agentic_rag.query_layer.agents.index_selector_agent import IndexSelectorAgent
from agentic_rag.query_layer.agents.memory_node import MemoryNode
from agentic_rag.query_layer.agents.planner_agent import PlannerAgent
from agentic_rag.query_layer.agents.query_decomposer import QueryDecomposer
from agentic_rag.query_layer.agents.query_rewriter import QueryRewriter
from agentic_rag.query_layer.agents.retrieval_controller_agent import RetrievalControllerAgent
from agentic_rag.reasoning_layer.graph.reasoning_graph import reasoning_graph
from agentic_rag.retrieval_layer.retrieval_pipeline import RetrievalPipeline

rewriter = QueryRewriter()
memory_agent = MemoryNode()
planner = PlannerAgent()
selector = IndexSelectorAgent()
controller = RetrievalControllerAgent()
executor = ExecutorAgent()
guardrail = ConversationGuardrail()
decomposer = QueryDecomposer()

retrieval_pipeline = RetrievalPipeline()


@traceable(name="guardrail_node")
def guardrail_node(state):
    result = guardrail.check(state["query"])
    print("🔹 Guardrail Decision:", result)

    if result["type"] == "conversational":
        print("💬 Conversational query detected")
        state["skip_retrieval"] = True
        state["answer"] = "Hello! How can I assist you today?"
    else:
        state["skip_retrieval"] = False

    return state


def memory_node(state):
    return memory_agent.run(state)


@traceable(name="rewrite_node")
def rewrite_node(state):
    if state["skip_retrieval"]:
        return state

    state["query"] = rewriter.run(state["query"])
    return state


@traceable(name="planner_node")
def planner_node(state):
    if state["skip_retrieval"]:
        return state

    state["plan"] = planner.run(state["query"])
    return state


@traceable(name="decomposition_node")
def decomposition_node(state):
    if state["skip_retrieval"]:
        return state

    state["subqueries"] = decomposer.run(state["query"], state["plan"])
    return state


@traceable(name="selector_node")
def selector_node(state):
    if state["skip_retrieval"]:
        return state

    state["index"] = selector.run(state["query"], state["plan"])
    return state


@traceable(name="controller_node")
def controller_node(state):
    if state["skip_retrieval"]:
        return state

    params = controller.run(
        state["query"],
        state["index"],
        state["plan"].get("metadata_filters", {}),
    )
    state["retrieval_params"] = params
    return state


@traceable(name="retrieval_node")
def retrieval_node(state):
    if state["skip_retrieval"]:
        return state

    docs = retrieval_pipeline.run(
        query=state["query"],
        index=state["index"],
        top_k=state["retrieval_params"]["top_k"],
        filters=state["retrieval_params"]["metadata_filter"],
    )
    state["docs"] = docs
    return state


@traceable(name="reasoning_wrapper")
def reasoning_wrapper(state):
    if state.get("skip_retrieval"):
        if "docs" not in state:
            state["docs"] = []
        return state

    if "docs" not in state:
        state["docs"] = []

    print("\n==============================")
    print("🧠 REASONING WRAPPER START")
    print("==============================")

    max_retry = 3
    iteration = 0

    while iteration < max_retry:
        print(f"\n🔁 Reasoning Iteration {iteration+1}")

        result = reasoning_graph.invoke(state)
        retry = result.get("retry", False)

        if not retry:
            print("✅ Reasoning validated answer")
            return result

        print("⚠ Reasoning requested retry")
        iteration += 1

        if iteration >= max_retry:
            print("❌ Max retry reached")
            return result

        print("🔄 Restarting pipeline from Query Rewrite")

        state["query"] = rewriter.run(state["query"])
        state["plan"] = planner.run(state["query"])
        state["index"] = selector.run(state["query"], state["plan"])

        params = controller.run(
            state["query"],
            state["index"],
            state["plan"].get("metadata_filters", {}),
        )
        state["retrieval_params"] = params

        docs = retrieval_pipeline.run(
            query=state["query"],
            index=state["index"],
            top_k=params["top_k"],
            filters=params["metadata_filter"],
        )
        state["docs"] = docs

        state["answer"] = executor.run(state["query"], docs)

    return state


@traceable(name="executor_node")
def executor_node(state):
    if state["skip_retrieval"]:
        return state

    state["answer"] = executor.run(state["query"], state["docs"])
    return state


builder = StateGraph(dict)

builder.add_node("guardrail", guardrail_node)
builder.add_node("rewrite", rewrite_node)
builder.add_node("memory", memory_node)
builder.add_node("decompose", decomposition_node)
builder.add_node("plan", planner_node)
builder.add_node("select_index", selector_node)
builder.add_node("controller", controller_node)
builder.add_node("retrieve", retrieval_node)
builder.add_node("execute", executor_node)
builder.add_node("reasoning_wrapper", reasoning_wrapper)
builder.add_node("reasoning_graph", reasoning_graph)

builder.set_entry_point("guardrail")

builder.add_edge("guardrail", "rewrite")
builder.add_edge("rewrite", "memory")
builder.add_edge("memory", "plan")
builder.add_edge("plan", "decompose")
builder.add_edge("decompose", "select_index")
builder.add_edge("select_index", "controller")
builder.add_edge("controller", "retrieve")
builder.add_edge("retrieve", "execute")
builder.add_edge("execute", "reasoning_wrapper")
builder.add_edge("reasoning_wrapper", "reasoning_graph")
builder.add_edge("reasoning_graph", END)

rag_graph = builder.compile()


if __name__ == "__main__":
    png = rag_graph.get_graph().draw_mermaid_png()

    with open("rag_graph.png", "wb") as f:
        f.write(png)

    os.startfile("rag_graph.png")
