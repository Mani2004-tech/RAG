# from langgraph.graph import StateGraph, END

# from agentic_rag.query_layer.agents.query_rewriter import QueryRewriter
# from agentic_rag.query_layer.agents.planner_agent import PlannerAgent
# from agentic_rag.query_layer.agents.index_selector_agent import IndexSelectorAgent
# from agentic_rag.query_layer.agents.retrieval_controller_agent import RetrievalControllerAgent
# from agentic_rag.query_layer.agents.executor_agent import ExecutorAgent
# from agentic_rag.query_layer.agents.conversation_guardrail import ConversationGuardrail

# from agentic_rag.retrieval_layer.retrieval_pipeline import RetrievalPipeline
# from agentic_rag.reasoning_layer.graph.reasoning_graph import reasoning_graph


# rewriter = QueryRewriter()
# planner = PlannerAgent()
# selector = IndexSelectorAgent()
# controller = RetrievalControllerAgent()
# executor = ExecutorAgent()

# guardrail = ConversationGuardrail()

# retrieval_pipeline = RetrievalPipeline()


# # ------------------------------
# # Guardrail Node
# # ------------------------------

# def guardrail_node(state):

#     result = guardrail.check(state["query"])

#     if result["type"] == "conversational":

#         state["skip_retrieval"] = True
#         state["answer"] = "Hello! How can I assist you today?"

#     else:

#         state["skip_retrieval"] = False

#     return state


# # ------------------------------
# # Rewrite Node
# # ------------------------------

# def rewrite_node(state):

#     if state["skip_retrieval"]:
#         return state

#     state["query"] = rewriter.run(state["query"])

#     return state


# # ------------------------------
# # Planner Node
# # ------------------------------

# def planner_node(state):

#     if state["skip_retrieval"]:
#         return state

#     state["plan"] = planner.run(state["query"])

#     return state


# # ------------------------------
# # Index Selector
# # ------------------------------

# def selector_node(state):

#     if state["skip_retrieval"]:
#         return state

#     state["index"] = selector.run(state["query"], state["plan"])

#     return state


# # ------------------------------
# # Retrieval Node
# # ------------------------------

# def retrieval_node(state):

#     if state["skip_retrieval"]:
#         return state

#     params = state.get("retrieval_params", {
#     "top_k": 5,
#     "metadata_filter": {}
# })

#     docs = retrieval_pipeline.run(
#         query=state["query"],
#         index=state["index"],
#         top_k=params["top_k"],
#         filters=params["metadata_filter"]
#     )

#     state["docs"] = docs

#     return state


# # ------------------------------
# # Executor
# # ------------------------------

# def executor_node(state):

#     if state["skip_retrieval"]:
#         return state

#     answer = executor.run(
#         state["query"],
#         state["docs"]
#     )

#     state["answer"] = answer

#     return state


# # ------------------------------
# # Reasoning Loop
# # ------------------------------

# def reasoning_node(state):

#     if state["skip_retrieval"]:
#         return state

#     result = reasoning_graph.invoke(state)

#     return result


# # ------------------------------
# # Build Graph
# # ------------------------------

# builder = StateGraph(dict)

# builder.add_node("guardrail", guardrail_node)
# builder.add_node("rewrite", rewrite_node)
# builder.add_node("plan", planner_node)
# builder.add_node("select_index", selector_node)
# builder.add_node("retrieve", retrieval_node)
# builder.add_node("execute", executor_node)
# builder.add_node("reason", reasoning_node)


# builder.set_entry_point("guardrail")

# builder.add_edge("guardrail", "rewrite")
# builder.add_edge("rewrite", "plan")
# builder.add_edge("plan", "select_index")
# builder.add_edge("select_index", "retrieve")
# builder.add_edge("retrieve", "execute")
# builder.add_edge("execute", "reason")
# builder.add_edge("reason", END)


# rag_graph = builder.compile()

from langsmith import traceable
from langgraph.graph import StateGraph, END

from agentic_rag.query_layer.agents.query_rewriter import QueryRewriter
from agentic_rag.query_layer.agents.planner_agent import PlannerAgent
from agentic_rag.query_layer.agents.index_selector_agent import IndexSelectorAgent
from agentic_rag.query_layer.agents.retrieval_controller_agent import RetrievalControllerAgent
from agentic_rag.query_layer.agents.executor_agent import ExecutorAgent
from agentic_rag.query_layer.agents.conversation_guardrail import ConversationGuardrail
from agentic_rag.query_layer.agents.memory_node import MemoryNode
from agentic_rag.retrieval_layer.retrieval_pipeline import RetrievalPipeline
from agentic_rag.reasoning_layer.graph.reasoning_graph import reasoning_graph
from agentic_rag.query_layer.agents.query_decomposer import QueryDecomposer

from graphviz import Digraph
import os


rewriter = QueryRewriter()
memory_agent = MemoryNode()
planner = PlannerAgent()
selector = IndexSelectorAgent()
controller = RetrievalControllerAgent()
executor = ExecutorAgent()
guardrail = ConversationGuardrail()
decomposer = QueryDecomposer()

retrieval_pipeline = RetrievalPipeline()


# ------------------------------
# Guardrail Node
# ------------------------------
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
# def guardrail_node(state):

#     result = guardrail.check(state["query"])

#     if result["type"] == "conversational":

#         state["skip_retrieval"] = True
#         state["answer"] = "Hello! How can I assist you today?"

#     else:

#         state["skip_retrieval"] = False

#     return state

def memory_node(state):
    return memory_agent.run(state)
# ------------------------------
# Rewrite
# ------------------------------
@traceable(name="rewrite_node")
def rewrite_node(state):

    if state["skip_retrieval"]:
        return state

    state["query"] = rewriter.run(state["query"])

    return state


# ------------------------------
# Planner
# ------------------------------
@traceable(name="planner_node")
def planner_node(state):

    if state["skip_retrieval"]:
        return state

    state["plan"] = planner.run(state["query"])

    return state

# ------------------------------
# Decomposition
# ------------------------------
@traceable(name="decomposition_node")
def decomposition_node(state):

    if state["skip_retrieval"]:
        return state

    subqueries = decomposer.run(
        state["query"],
        state["plan"]
    )

    state["subqueries"] = subqueries

    return state

# ------------------------------
# Index Selector
# ------------------------------
@traceable(name="selector_node")
def selector_node(state):

    if state["skip_retrieval"]:
        return state

    state["index"] = selector.run(state["query"], state["plan"])

    return state


# ------------------------------
# Retrieval Controller
# ------------------------------
@traceable(name="controller_node")
def controller_node(state):
    if state["skip_retrieval"]:
            return state

    params = controller.run(
        state["query"],
        state["index"],
        state["plan"].get("metadata_filters", {})
    )

    state["retrieval_params"] = params

    return state


# ------------------------------
# Retrieval
# ------------------------------
@traceable(name="retrieval_node")
def retrieval_node(state):

    if state["skip_retrieval"]:
        return state

    # params = state.get("retrieval_params", {
    #     "top_k": 5,
    #     "metadata_filter": {}
    # })

    docs = retrieval_pipeline.run(
        query=state["query"],
        index=state["index"],
        top_k=state["retrieval_params"]["top_k"],
        filters=state["retrieval_params"]["metadata_filter"]
    )

    state["docs"] = docs

    return state
# ------------------------------
# Reasoning Loop
# ------------------------------
# @traceable(name="reasoning_wrapper")
# def reasoning_wrapper(state):

#     # conversational query
#     if state.get("skip_retrieval"):

#         # ensure reasoning graph does not crash
#         if "docs" not in state:
#             state["docs"] = []

#         return state

#     # retrieval not executed
#     if "docs" not in state:
#         state["docs"] = []

#     return state
@traceable(name="reasoning_wrapper")
def reasoning_wrapper(state):

    # conversational queries
    if state.get("skip_retrieval"):

        if "docs" not in state:
            state["docs"] = []

        return state

    # ensure docs exist
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

        # restart pipeline from rewrite node
        state["query"] = rewriter.run(state["query"])

        state["plan"] = planner.run(state["query"])

        state["index"] = selector.run(state["query"], state["plan"])

        params = controller.run(
            state["query"],
            state["index"],
            state["plan"].get("metadata_filters", {})
        )

        state["retrieval_params"] = params

        docs = retrieval_pipeline.run(
            query=state["query"],
            index=state["index"],
            top_k=params["top_k"],
            filters=params["metadata_filter"]
        )

        state["docs"] = docs

        state["answer"] = executor.run(
            state["query"],
            docs
        )

    return state
# ------------------------------
# Executor
# ------------------------------
@traceable(name="executor_node")
def executor_node(state):

    if state["skip_retrieval"]:
        return state

    answer = executor.run(
        state["query"],
        state["docs"]
    )

    state["answer"] = answer

    return state



# ------------------------------
# Build Graph
# ------------------------------

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
# builder.add_node("reason", reasoning_node)
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
# builder.add_edge("execute", "reason")
# builder.add_edge("reason", END)
builder.add_edge("execute", "reasoning_wrapper")
builder.add_edge("reasoning_wrapper", "reasoning_graph")
builder.add_edge("reasoning_graph", END)
# builder.add_edge("execute", "reasoning_graph")

# builder.add_edge("reasoning_graph", END)

rag_graph = builder.compile()

from IPython.display import Image, display
import os

if __name__ == "__main__":

    png = rag_graph.get_graph().draw_mermaid_png()

    with open("rag_graph.png", "wb") as f:
        f.write(png)

    os.startfile("rag_graph.png")


# png = rag_graph.get_graph().draw_mermaid_png()

# with open("rag_graph.png", "wb") as f:
#     f.write(png)

# os.startfile("rag_graph.png")   # Windows

# import networkx as nx
# import matplotlib.pyplot as plt


# def hierarchical_layout(G, root):

#     levels = {root: 0}
#     queue = [root]

#     while queue:
#         node = queue.pop(0)
#         for child in G.successors(node):
#             if child not in levels:
#                 levels[child] = levels[node] + 1
#                 queue.append(child)

#     level_nodes = {}
#     for node, level in levels.items():
#         level_nodes.setdefault(level, []).append(node)

#     pos = {}
#     for level, nodes in level_nodes.items():
#         width = len(nodes)
#         for i, node in enumerate(nodes):
#             pos[node] = (i - width / 2, -level)

#     return pos


# def render_tree_graph(rag_graph):

#     graph = rag_graph.get_graph()

#     G = nx.DiGraph()

#     for node in graph.nodes:
#         G.add_node(str(node))

#     for edge in graph.edges:
#         src = str(edge[0])
#         dst = str(edge[1])
#         G.add_edge(src, dst)

#     root = "__start__"

#     pos = hierarchical_layout(G, root)

#     plt.figure(figsize=(14,10))

#     nx.draw(
#         G,
#         pos,
#         with_labels=True,
#         node_size=3000,
#         node_color="#8fbcd4",
#         arrows=True,
#         font_size=9
#     )

#     plt.title("Agentic RAG Execution Tree")

#     plt.savefig("rag_execution_graph.png")
#     plt.close()

#     print("✅ Tree graph generated")
# render_tree_graph(rag_graph)