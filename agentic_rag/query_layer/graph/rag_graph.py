# # from langgraph.graph import StateGraph, END

# # from agentic_rag.query_layer.agents.query_rewriter import QueryRewriter
# # from agentic_rag.query_layer.agents.planner_agent import PlannerAgent
# # from agentic_rag.query_layer.agents.index_selector_agent import IndexSelectorAgent
# # from agentic_rag.query_layer.agents.retrieval_controller_agent import RetrievalControllerAgent
# # from agentic_rag.query_layer.agents.executor_agent import ExecutorAgent
# # from agentic_rag.query_layer.agents.conversation_guardrail import ConversationGuardrail

# # from agentic_rag.retrieval_layer.retrieval_pipeline import RetrievalPipeline
# # from agentic_rag.reasoning_layer.graph.reasoning_graph import reasoning_graph


# # rewriter = QueryRewriter()
# # planner = PlannerAgent()
# # selector = IndexSelectorAgent()
# # controller = RetrievalControllerAgent()
# # executor = ExecutorAgent()

# # guardrail = ConversationGuardrail()

# # retrieval_pipeline = RetrievalPipeline()


# # # ------------------------------
# # # Guardrail Node
# # # ------------------------------

# # def guardrail_node(state):

# #     result = guardrail.check(state["query"])

# #     if result["type"] == "conversational":

# #         state["skip_retrieval"] = True
# #         state["answer"] = "Hello! How can I assist you today?"

# #     else:

# #         state["skip_retrieval"] = False

# #     return state


# # # ------------------------------
# # # Rewrite Node
# # # ------------------------------

# # def rewrite_node(state):

# #     if state["skip_retrieval"]:
# #         return state

# #     state["query"] = rewriter.run(state["query"])

# #     return state


# # # ------------------------------
# # # Planner Node
# # # ------------------------------

# # def planner_node(state):

# #     if state["skip_retrieval"]:
# #         return state

# #     state["plan"] = planner.run(state["query"])

# #     return state


# # # ------------------------------
# # # Index Selector
# # # ------------------------------

# # def selector_node(state):

# #     if state["skip_retrieval"]:
# #         return state

# #     state["index"] = selector.run(state["query"], state["plan"])

# #     return state


# # # ------------------------------
# # # Retrieval Node
# # # ------------------------------

# # def retrieval_node(state):

# #     if state["skip_retrieval"]:
# #         return state

# #     params = state.get("retrieval_params", {
# #     "top_k": 5,
# #     "metadata_filter": {}
# # })

# #     docs = retrieval_pipeline.run(
# #         query=state["query"],
# #         index=state["index"],
# #         top_k=params["top_k"],
# #         filters=params["metadata_filter"]
# #     )

# #     state["docs"] = docs

# #     return state


# # # ------------------------------
# # # Executor
# # # ------------------------------

# # def executor_node(state):

# #     if state["skip_retrieval"]:
# #         return state

# #     answer = executor.run(
# #         state["query"],
# #         state["docs"]
# #     )

# #     state["answer"] = answer

# #     return state


# # # ------------------------------
# # # Reasoning Loop
# # # ------------------------------

# # def reasoning_node(state):

# #     if state["skip_retrieval"]:
# #         return state

# #     result = reasoning_graph.invoke(state)

# #     return result


# # # ------------------------------
# # # Build Graph
# # # ------------------------------

# # builder = StateGraph(dict)

# # builder.add_node("guardrail", guardrail_node)
# # builder.add_node("rewrite", rewrite_node)
# # builder.add_node("plan", planner_node)
# # builder.add_node("select_index", selector_node)
# # builder.add_node("retrieve", retrieval_node)
# # builder.add_node("execute", executor_node)
# # builder.add_node("reason", reasoning_node)


# # builder.set_entry_point("guardrail")

# # builder.add_edge("guardrail", "rewrite")
# # builder.add_edge("rewrite", "plan")
# # builder.add_edge("plan", "select_index")
# # builder.add_edge("select_index", "retrieve")
# # builder.add_edge("retrieve", "execute")
# # builder.add_edge("execute", "reason")
# # builder.add_edge("reason", END)


# # rag_graph = builder.compile()

# from langsmith import traceable
# from langgraph.graph import StateGraph, END

# from agentic_rag.query_layer.agents.query_rewriter import QueryRewriter
# from agentic_rag.query_layer.agents.planner_agent import PlannerAgent
# from agentic_rag.query_layer.agents.index_selector_agent import IndexSelectorAgent
# from agentic_rag.query_layer.agents.retrieval_controller_agent import RetrievalControllerAgent
# from agentic_rag.query_layer.agents.executor_agent import ExecutorAgent
# from agentic_rag.query_layer.agents.conversation_guardrail import ConversationGuardrail
# from agentic_rag.query_layer.agents.memory_node import MemoryNode
# from agentic_rag.retrieval_layer.retrieval_pipeline import RetrievalPipeline
# from agentic_rag.reasoning_layer.graph.reasoning_graph import reasoning_graph
# from agentic_rag.query_layer.agents.query_decomposer import QueryDecomposer


# rewriter = QueryRewriter()
# memory_agent = MemoryNode()
# planner = PlannerAgent()
# selector = IndexSelectorAgent()
# controller = RetrievalControllerAgent()
# executor = ExecutorAgent()
# guardrail = ConversationGuardrail()
# decomposer = QueryDecomposer()

# retrieval_pipeline = RetrievalPipeline()


# # ------------------------------
# # Guardrail Node
# # ------------------------------
# @traceable(name="guardrail_node")
# def guardrail_node(state):

#     result = guardrail.check(state["query"])

#     if result["type"] == "conversational":

#         state["skip_retrieval"] = True
#         state["answer"] = "Hello! How can I assist you today?"

#     else:

#         state["skip_retrieval"] = False

#     return state

# def memory_node(state):
#     if state["skip_retrieval"]:
#         return state

#     return memory_agent.run(state)
# # ------------------------------
# # Rewrite
# # ------------------------------
# @traceable(name="rewrite_node")
# def rewrite_node(state):

#     if state["skip_retrieval"]:
#         return state

#     state["query"] = rewriter.run(state["query"])

#     return state


# # ------------------------------
# # Planner
# # ------------------------------
# @traceable(name="planner_node")
# def planner_node(state):

#     if state["skip_retrieval"]:
#         return state

#     state["plan"] = planner.run(state["query"])

#     return state

# # ------------------------------
# # Decomposition
# # ------------------------------
# @traceable(name="decomposition_node")
# def decomposition_node(state):

#     if state["skip_retrieval"]:
#         return state

#     subqueries = decomposer.run(
#         state["query"],
#         state["plan"]
#     )

#     state["subqueries"] = subqueries

#     return state

# # ------------------------------
# # Index Selector
# # ------------------------------
# @traceable(name="selector_node")
# def selector_node(state):

#     if state["skip_retrieval"]:
#         return state

#     state["index"] = selector.run(state["query"], state["plan"])

#     return state


# # ------------------------------
# # Retrieval Controller
# # ------------------------------
# @traceable(name="controller_node")
# def controller_node(state):
#     if state["skip_retrieval"]:
#             return state

#     params = controller.run(
#         state["query"],
#         state["index"],
#         state["plan"].get("metadata_filters", {})
#     )

#     state["retrieval_params"] = params

#     return state


# # ------------------------------
# # Retrieval
# # ------------------------------
# @traceable(name="retrieval_node")
# def retrieval_node(state):

#     if state["skip_retrieval"]:
#         return state

#     # params = state.get("retrieval_params", {
#     #     "top_k": 5,
#     #     "metadata_filter": {}
#     # })

#     docs = retrieval_pipeline.run(
#         query=state["query"],
#         index=state["index"],
#         top_k=state["retrieval_params"]["top_k"],
#         filters=state["retrieval_params"]["metadata_filter"]
#     )

#     state["docs"] = docs

#     return state


# # ------------------------------
# # Executor
# # ------------------------------
# @traceable(name="executor_node")
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
# @traceable(name="reasoning_node")
# def reasoning_node(state):

#     if state["skip_retrieval"]:
#         return state

#     print("\n==============================")
#     print("🧠 REASONING NODE START")
#     print("==============================")

#     answer = state["answer"]

#     if "Information not found" not in answer:

#         print("✅ Answer found — skipping reasoning loop")

#         return state

#     print("⚠ Answer missing, forcing retry reasoning")

#     max_retry = 3
#     iteration = 0

#     while iteration < max_retry:

#         print(f"\n🔁 Reasoning Iteration {iteration+1}")

#         result = reasoning_graph.invoke(state)

#         retry = result.get("retry", False)

#         if not retry:

#             print("✅ Reasoning validated answer")

#             return result

#         print("⚠ Answer invalid — retrying retrieval")

#         docs = retrieval_pipeline.run(
#             query=state["query"],
#             index=state["index"],
#             top_k=state["retrieval_params"]["top_k"],
#             filters=state["retrieval_params"]["metadata_filter"]
#         )

#         state["docs"] = docs

#         answer = executor.run(
#             state["query"],
#             docs
#         )

#         state["answer"] = answer

#         iteration += 1

#     print("❌ Max reasoning retries reached")

#     print("🧠 REASONING NODE END\n")

#     return state

# # ------------------------------
# # Build Graph
# # ------------------------------

# builder = StateGraph(dict)

# builder.add_node("guardrail", guardrail_node)
# builder.add_node("rewrite", rewrite_node)
# builder.add_node("memory", memory_node)
# builder.add_node("decompose", decomposition_node)
# builder.add_node("plan", planner_node)
# builder.add_node("select_index", selector_node)
# builder.add_node("controller", controller_node)
# builder.add_node("retrieve", retrieval_node)
# builder.add_node("execute", executor_node)
# builder.add_node("reason", reasoning_node)

# builder.set_entry_point("guardrail")

# builder.add_edge("guardrail", "rewrite")
# builder.add_edge("rewrite", "memory")
# builder.add_edge("memory", "plan")
# builder.add_edge("plan", "decompose")
# builder.add_edge("decompose", "select_index")
# builder.add_edge("select_index", "controller")
# builder.add_edge("controller", "retrieve")
# builder.add_edge("retrieve", "execute")
# builder.add_edge("execute", "reason")
# builder.add_edge("reason", END)

# rag_graph = builder.compile()


# from IPython.display import Image, display
# import os

# png = rag_graph.get_graph().draw_mermaid_png()

# with open("rag_graph.png", "wb") as f:
#     f.write(png)

# os.startfile("rag_graph.png")   # Windows
# from langsmith import traceable
# from langgraph.graph import StateGraph, END

# from agentic_rag.query_layer.agents.query_rewriter import QueryRewriter
# from agentic_rag.query_layer.agents.planner_agent import PlannerAgent
# from agentic_rag.query_layer.agents.index_selector_agent import IndexSelectorAgent
# from agentic_rag.query_layer.agents.retrieval_controller_agent import RetrievalControllerAgent
# from agentic_rag.query_layer.agents.executor_agent import ExecutorAgent
# from agentic_rag.query_layer.agents.conversation_guardrail import ConversationGuardrail
# from agentic_rag.query_layer.agents.memory_node import MemoryNode
# from agentic_rag.retrieval_layer.retrieval_pipeline import RetrievalPipeline
# from agentic_rag.reasoning_layer.graph.reasoning_graph import reasoning_graph
# from agentic_rag.query_layer.agents.query_decomposer import QueryDecomposer


# # ------------------------------
# # INIT AGENTS
# # ------------------------------

# rewriter = QueryRewriter()
# memory_agent = MemoryNode()
# planner = PlannerAgent()
# selector = IndexSelectorAgent()
# controller = RetrievalControllerAgent()
# executor = ExecutorAgent()
# guardrail = ConversationGuardrail()
# decomposer = QueryDecomposer()

# retrieval_pipeline = RetrievalPipeline()


# # ------------------------------
# # NODES (NO ROUTING LOGIC HERE)
# # ------------------------------

# @traceable(name="guardrail_node")
# def guardrail_node(state):

#     result = guardrail.check(state["query"])

#     if result["type"] == "conversational":
#         state["skip_retrieval"] = True
#         state["answer"] = "Hello! How can I assist you today?"
#     else:
#         state["skip_retrieval"] = False

#     return state


# @traceable(name="rewrite_node")
# def rewrite_node(state):

#     state["query"] = rewriter.run(state["query"])

#     return state


# def memory_node(state):

#     return memory_agent.run(state)


# @traceable(name="planner_node")
# def planner_node(state):

#     state["plan"] = planner.run(state["query"])

#     return state


# @traceable(name="decomposition_node")
# def decomposition_node(state):

#     subqueries = decomposer.run(
#         state["query"],
#         state["plan"]
#     )

#     state["subqueries"] = subqueries

#     return state


# @traceable(name="selector_node")
# def selector_node(state):

#     state["index"] = selector.run(state["query"], state["plan"])

#     return state


# @traceable(name="controller_node")
# def controller_node(state):

#     params = controller.run(
#         state["query"],
#         state["index"],
#         state["plan"].get("metadata_filters", {})
#     )

#     state["retrieval_params"] = params

#     return state


# @traceable(name="retrieval_node")
# def retrieval_node(state):

#     params = state["retrieval_params"]

#     docs = retrieval_pipeline.run(
#         query=state["query"],
#         index=state["index"],
#         top_k=params["top_k"],
#         filters=params["metadata_filter"]
#     )

#     state["docs"] = docs

#     return state


# @traceable(name="executor_node")
# def executor_node(state):

#     answer = executor.run(
#         state["query"],
#         state["docs"]
#     )

#     state["answer"] = answer

#     return state


# @traceable(name="reasoning_node")
# def reasoning_node(state):

#     print("\n🧠 REASONING NODE")

#     result = reasoning_graph.invoke(state)

#     state.update(result)

#     return state


# # ------------------------------
# # BUILD GRAPH
# # ------------------------------

# builder = StateGraph(dict)

# builder.add_node("guardrail", guardrail_node)
# builder.add_node("rewrite", rewrite_node)
# builder.add_node("memory", memory_node)
# builder.add_node("plan", planner_node)
# builder.add_node("decompose", decomposition_node)
# builder.add_node("select_index", selector_node)
# builder.add_node("controller", controller_node)
# builder.add_node("retrieve", retrieval_node)
# builder.add_node("execute", executor_node)
# builder.add_node("reason", reasoning_node)

# builder.set_entry_point("guardrail")


# # ------------------------------
# # CONDITIONAL ROUTING
# # ------------------------------

# # 1️⃣ Guardrail routing
# def guardrail_router(state):

#     if state.get("skip_retrieval"):
#         return "end"

#     return "rewrite"


# builder.add_conditional_edges(
#     "guardrail",
#     guardrail_router,
#     {
#         "rewrite": "rewrite",
#         "end": END
#     }
# )


# # 2️⃣ Memory routing
# def memory_router(state):

#     if state.get("skip_retrieval"):
#         return "end"

#     return "plan"


# builder.add_conditional_edges(
#     "memory",
#     memory_router,
#     {
#         "plan": "plan",
#         "end": END
#     }
# )


# # ------------------------------
# # NORMAL FLOW
# # ------------------------------

# builder.add_edge("rewrite", "memory")
# builder.add_edge("plan", "decompose")
# builder.add_edge("decompose", "select_index")
# builder.add_edge("select_index", "controller")
# builder.add_edge("controller", "retrieve")
# builder.add_edge("retrieve", "execute")
# builder.add_edge("execute", "reason")


# # ------------------------------
# # REASONING LOOP (KEY PART)
# # ------------------------------

# def reasoning_router(state):

#     if state.get("retry", False):
#         return "retry"

#     return "end"


# builder.add_conditional_edges(
#     "reason",
#     reasoning_router,
#     {
#         "retry": "retrieve",
#         "end": END
#     }
# )


# # ------------------------------
# # COMPILE
# # ------------------------------

# rag_graph = builder.compile()

from langsmith import traceable
from langgraph.graph import StateGraph, END
import random
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


# ✅ NEW: MAX RETRY LIMIT
MAX_RETRIES = 2

ADAPTIVE_RETRIEVAL_ORDER = [
    "vector",
    "hybrid",
    "knowledge_graph"
]


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
# NODES
# ------------------------------

@traceable(name="guardrail_node")
def guardrail_node(state):

    result = guardrail.check(state["query"])
    intent = result["intent"]

    state["intent"] = intent

    if intent in ["conversational", "meta"]:
        state["skip_retrieval"] = True

        responses = {
            "conversational": [
                "Hey! What can I help you with?",
                "Hello! How can I assist you today?",
                "Hi there!"
            ],
            "meta": [
                "I'm your AI assistant. I can help with questions and problem solving.",
                "I’m an AI system designed to help you with information and tasks."
            ]
        }

        
        state["answer"] = random.choice(responses[intent])

    elif intent == "harmful":
        state["skip_retrieval"] = True
        state["answer"] = "I can't assist with that request."

    else:
        state["skip_retrieval"] = False
    

    return state


@traceable(name="rewrite_node")
def rewrite_node(state):

    state["query"] = rewriter.run(state["query"])
    return state


def memory_node(state):
    return memory_agent.run(state)


@traceable(name="planner_node")
def planner_node(state):

    state["plan"] = planner.run(state["query"])
    return state


@traceable(name="decomposition_node")
def decomposition_node(state):

    state["subqueries"] = decomposer.run(
        state["query"],
        state["plan"]
    )
    return state


@traceable(name="selector_node")
def selector_node(state):

    state["index"] = selector.run(state["query"], state["plan"])
    return state


@traceable(name="controller_node")
def controller_node(state):

    state["retrieval_params"] = controller.run(
        state["query"],
        state["index"],
        state["plan"].get("metadata_filters", {})
    )
    return state


@traceable(name="retrieval_node")
def retrieval_node(state):

    params = state["retrieval_params"]

    state["docs"] = retrieval_pipeline.run(
        query=state["query"],
        index=state["index"],
        top_k=params["top_k"],
        filters=params["metadata_filter"]
    )

    return state


@traceable(name="executor_node")
def executor_node(state):

    result = executor.run(
        state["query"],
        state["docs"],
        state.get("chat_history", [])
    )

    state["answer"] = result["answer"]
    state["retrieval_failed"] = result["retrieval_failed"]

    return state


# ✅ UPDATED: reasoning node with iteration counter
@traceable(name="reasoning_node")
def reasoning_node(state):

    print("\n🧠 REASONING NODE")

    # ------------------------------
    # ✅ INIT ITERATION (DO NOT COUNT FIRST PASS)
    # ------------------------------
    iteration = state.get("iteration", 0)

    print(f"🔁 Current Iteration: {iteration}")

    # ------------------------------
    # ✅ SWITCH ONLY ON RETRIES
    # ------------------------------
    if iteration > 0 and iteration <= len(ADAPTIVE_RETRIEVAL_ORDER):

        new_index = ADAPTIVE_RETRIEVAL_ORDER[iteration - 1]

        print(f"🔄 Switching Retrieval Strategy → {new_index}")

        state["index"] = new_index

    # ------------------------------
    # ✅ RUN REASONING (ALWAYS)
    # ------------------------------
    result = reasoning_graph.invoke(state)

    state.update(result)

    # ------------------------------
    # ✅ INCREMENT ONLY IF RETRY
    # ------------------------------
    if state.get("retry", False):
        state["iteration"] = iteration + 1

    return state

# ------------------------------
# BUILD GRAPH
# ------------------------------

builder = StateGraph(dict)

builder.add_node("guardrail", guardrail_node)
builder.add_node("rewrite", rewrite_node)
builder.add_node("memory", memory_node)
builder.add_node("plan", planner_node)
builder.add_node("decompose", decomposition_node)
builder.add_node("select_index", selector_node)
builder.add_node("controller", controller_node)
builder.add_node("retrieve", retrieval_node)
builder.add_node("execute", executor_node)
builder.add_node("reason", reasoning_node)

builder.set_entry_point("guardrail")


# ------------------------------
# CONDITIONAL EDGES
# ------------------------------

# guardrail routing
def guardrail_router(state):
    return "end" if state.get("skip_retrieval") else "rewrite"

builder.add_conditional_edges(
    "guardrail",
    guardrail_router,
    {
        "rewrite": "rewrite",
        "end": END
    }
)

# memory routing
def memory_router(state):
    return "end" if state.get("skip_retrieval") else "plan"

builder.add_conditional_edges(
    "memory",
    memory_router,
    {
        "plan": "plan",
        "end": END
    }
)

# normal flow
builder.add_edge("rewrite", "memory")
builder.add_edge("plan", "decompose")
builder.add_edge("decompose", "select_index")
builder.add_edge("select_index", "controller")
builder.add_edge("controller", "retrieve")
builder.add_edge("retrieve", "execute")
builder.add_edge("execute", "reason")



# def reasoning_router(state):

#     iteration = state.get("iteration", 0)
#     retry = state.get("retry", False)

#     print("\n🔹 Reasoning Router")
#     print("Iteration:", iteration)
#     print("Retry:", retry)

#     if iteration >= MAX_RETRIES:
#         print("❌ Max retries reached")
#         return "end"

#     if retry:
#         print("🔁 Retrying retrieval")
#         return "retry"

#     print("✅ Answer accepted")
#     return "end"
# ✅ UPDATED: reasoning router with retry limit
def reasoning_router(state):

    iteration = state.get("iteration", 0)
    retry = state.get("retry", False)

    print("\n🔹 Reasoning Router")
    print("Iteration:", iteration)
    print("Retry:", retry)
    print("Current Index:", state.get("index"))

    if iteration >= MAX_RETRIES:
        print("❌ Max retries reached → END")
        return "end"

    if retry:
        print("🔁 Retry with next retrieval strategy")
        return "retry"

    print("✅ Answer accepted → END")
    return "end"

builder.add_conditional_edges(
    "reason",
    reasoning_router,
    {
        "retry": "controller",  # ✅ FIX: go through controller again
        "end": END
    }
)

rag_graph = builder.compile()
# ------------------------------
# OPTIONAL GRAPH VISUALIZATION
# ------------------------------

from IPython.display import Image
import os

png = rag_graph.get_graph().draw_mermaid_png()

with open("rag_graph.png", "wb") as f:
    f.write(png)

os.startfile("rag_graph.png")