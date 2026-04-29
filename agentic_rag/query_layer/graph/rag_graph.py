
# from langsmith import traceable
# from langgraph.graph import StateGraph, END
# import random
# from agentic_rag.langfuse_client import langfuse  # ✅ ADDED
# from agentic_rag.query_layer.agents.query_rewriter import QueryRewriter
# from agentic_rag.query_layer.agents.planner_agent import PlannerAgent
# from agentic_rag.query_layer.agents.index_selector_agent import IndexSelectorAgent
# from agentic_rag.query_layer.agents.retrieval_controller_agent import RetrievalControllerAgent
# from agentic_rag.query_layer.agents.executor_agent import ExecutorAgent
# from agentic_rag.query_layer.agents.conversation_guardrail import ConversationGuardrail
# from agentic_rag.query_layer.agents.memory_node import MemoryNode
# from agentic_rag.retrieval_layer.retrieval_pipeline import RetrievalPipeline
# from agentic_rag.reasoning_layer.graph.reasoning_graph import reasoning_graph
# from agentic_rag.evaluation_layer.evaluation_service import EvaluationService
# from agentic_rag.query_layer.agents.query_decomposer import QueryDecomposer


# # ✅ NEW: MAX RETRY LIMIT
# MAX_RETRIES = 2

# ADAPTIVE_RETRIEVAL_ORDER = [
#     "vector",
#     "hybrid",
#     "knowledge_graph"
# ]


# rewriter = QueryRewriter()
# memory_agent = MemoryNode()
# planner = PlannerAgent()
# selector = IndexSelectorAgent()
# controller = RetrievalControllerAgent()
# executor = ExecutorAgent()
# guardrail = ConversationGuardrail()
# decomposer = QueryDecomposer()
# evaluator = EvaluationService()
# retrieval_pipeline = RetrievalPipeline()


# # ------------------------------
# # NODES
# # ------------------------------

# @traceable(name="guardrail_node")
# def guardrail_node(state):
#     lf = langfuse.trace(name="guardrail_node", input=state)  # ✅ ADDED
#     result = guardrail.check(state["query"])
#     intent = result["intent"]

#     state["intent"] = intent

#     if intent in ["conversational", "meta"]:
#         state["skip_retrieval"] = True

#         responses = {
#             "conversational": [
#                 "Hey! What can I help you with?",
#                 "Hello! How can I assist you today?",
#                 "Hi there!"
#             ],
#             "meta": [
#                 "I'm your AI assistant. I can help with questions and problem solving.",
#                 "I’m an AI system designed to help you with information and tasks."
#             ]
#         }

        
#         state["answer"] = random.choice(responses[intent])

#     elif intent == "harmful":
#         state["skip_retrieval"] = True
#         state["answer"] = "I can't assist with that request."

#     else:
#         state["skip_retrieval"] = False
    
#     lf.end(output=state)  # ✅ ADDED
#     return state


# @traceable(name="rewrite_node")
# def rewrite_node(state):
#     lf = langfuse.trace(name="rewrite_node", input=state)  # ✅ ADDED
#     state["query"] = rewriter.run(state["query"])
#     lf.end(output=state)  # ✅ ADDED
#     return state


# def memory_node(state):
#     lf = langfuse.trace(name="memory_node", input=state)  # ✅ ADDED
#     # return memory_agent.run(state)
#     result = memory_agent.run(state)

#     lf.end(output=result)  # ✅ ADDED
#     return result



# @traceable(name="planner_node")
# def planner_node(state):
#     lf = langfuse.trace(name="planner_node", input=state)  # ✅ ADDED
#     state["plan"] = planner.run(state["query"])
#     lf.end(output=state)  # ✅ ADDED
#     return state


# @traceable(name="decomposition_node")
# def decomposition_node(state):
#     lf = langfuse.trace(name="decomposition_node", input=state)  # ✅ ADDED
#     state["subqueries"] = decomposer.run(
#         state["query"],
#         state["plan"]
#     )
#     lf.end(output=state)  # ✅ ADDED
#     return state


# @traceable(name="selector_node")
# def selector_node(state):
#     lf = langfuse.trace(name="selector_node", input=state)  # ✅ ADDED
#     state["index"] = selector.run(state["query"], state["plan"])
#     lf.end(output=state)  # ✅ ADDED
#     return state


# @traceable(name="controller_node")
# def controller_node(state):
#     lf = langfuse.trace(name="controller_node", input=state)  # ✅ ADDED
#     state["retrieval_params"] = controller.run(
#         state["query"],
#         state["index"],
#         state["plan"].get("metadata_filters", {})
#     )
#     lf.end(output=state)  # ✅ ADDED
#     return state


# @traceable(name="retrieval_node")
# def retrieval_node(state):
#     lf = langfuse.trace(name="retrieval_node", input=state)  # ✅ ADDED
#     params = state["retrieval_params"]

#     state["docs"] = retrieval_pipeline.run(
#         query=state["query"],
#         index=state["index"],
#         top_k=params["top_k"],
#         filters=params["metadata_filter"]
#     )
#     lf.end(output=state)  # ✅ ADDED
#     return state


# @traceable(name="executor_node")
# def executor_node(state):
#     lf = langfuse.trace(name="executor_node", input=state)  # ✅ ADDED
#     result = executor.run(
#         state["query"],
#         state["docs"],
#         state.get("chat_history", [])
#     )

#     state["answer"] = result["answer"]
#     state["retrieval_failed"] = result["retrieval_failed"]
#     lf.end(output=state)  # ✅ ADDED
#     return state


# # ✅ UPDATED: reasoning node with iteration counter
# @traceable(name="reasoning_node")
# def reasoning_node(state):
#     lf = langfuse.trace(name="reasoning_node", input=state)  # ✅ ADDED
#     print("\n🧠 REASONING NODE")

#     iteration = state.get("iteration", 0)

#     print(f"🔁 Current Iteration: {iteration}")

#     # ------------------------------
#     # SWITCH RETRIEVAL STRATEGY
#     # ------------------------------
#     if iteration > 0 and iteration <= len(ADAPTIVE_RETRIEVAL_ORDER):

#         new_index = ADAPTIVE_RETRIEVAL_ORDER[iteration - 1]

#         print(f"🔄 Switching Retrieval Strategy → {new_index}")

#         state["index"] = new_index

#     # ------------------------------
#     # RUN REASONING
#     # ------------------------------
#     result = reasoning_graph.invoke(state)

#     state.update(result)

#     # ------------------------------
#     # ✅ FIX 1: STOP IF VALID
#     # ------------------------------
#     if state.get("valid", False):
#         print("✅ Answer validated → stopping loop")
#         state["retry"] = False
#         return state

#     # ------------------------------
#     # ✅ FIX 2: SAFE ITERATION INCREMENT
#     # ------------------------------
#     if state.get("retry", False):

#         next_iteration = iteration + 1
#         state["iteration"] = next_iteration

#         print(f"🔁 Next Iteration Prepared: {next_iteration}")

#         if next_iteration >= MAX_RETRIES:
#             print("🛑 Max retries reached → stopping loop")
#             state["retry"] = False
#     lf.end(output=state)  # ✅ ADDED
#     return state

# @traceable(name="evaluation_node")
# def evaluation_node(state):
#     lf = langfuse.trace(name="evaluation_node", input=state)  # ✅ ADDED
#     print("\n📊 EVALUATION NODE")

#     try:
#         result = evaluator.run(
#             state["query"],
#             state["answer"],
#             state.get("docs", [])
#         )

#         state["evaluation"] = result

#     except Exception as e:
#         print("⚠ Evaluation failed:", e)
#     lf.end(output=state)  # ✅ ADDED
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
# builder.add_node("evaluation", evaluation_node)

# builder.set_entry_point("guardrail")


# # ------------------------------
# # CONDITIONAL EDGES
# # ------------------------------

# # guardrail routing
# def guardrail_router(state):
#     return "end" if state.get("skip_retrieval") else "rewrite"

# builder.add_conditional_edges(
#     "guardrail",
#     guardrail_router,
#     {
#         "rewrite": "rewrite",
#         "end": END
#     }
# )

# # memory routing
# def memory_router(state):
#     return "end" if state.get("skip_retrieval") else "plan"

# builder.add_conditional_edges(
#     "memory",
#     memory_router,
#     {
#         "plan": "plan",
#         "end": END
#     }
# )

# # normal flow
# builder.add_edge("rewrite", "memory")
# builder.add_edge("plan", "decompose")
# builder.add_edge("decompose", "select_index")
# builder.add_edge("select_index", "controller")
# builder.add_edge("controller", "retrieve")
# builder.add_edge("retrieve", "execute")
# builder.add_edge("execute", "reason")
# # builder.add_edge("evaluation", END)



# def reasoning_router(state):

#     iteration = state.get("iteration", 0)
#     retry = state.get("retry", False)

#     print("\n🔹 Reasoning Router")
#     print("Iteration:", iteration)
#     print("Retry:", retry)
#     print("Current Index:", state.get("index"))

#     if iteration >= MAX_RETRIES:
#         print("❌ Max retries reached → END")
#         return "end"

#     if retry:
#         print("🔁 Retry with next retrieval strategy")
#         return "retry"

#     print("✅ Answer accepted → END")
#     return "end"

# builder.add_conditional_edges(
#     "reason",
#     reasoning_router,
#     {
#         "retry": "controller",  # ✅ FIX: go through controller again
#         "end": END
#     }
# )

# rag_graph = builder.compile()
# # ------------------------------
# # OPTIONAL GRAPH VISUALIZATION
# # ------------------------------

# # from IPython.display import Image
# # import os

# # png = rag_graph.get_graph().draw_mermaid_png()

# # with open("rag_graph.png", "wb") as f:
# #     f.write(png)

# # os.startfile("rag_graph.png")

# from IPython.display import Image
# import os


# print("🎯 Generating RAG Graph Image...")

# png = rag_graph.get_graph().draw_mermaid_png()

# with open("rag_graph.png", "wb") as f:
#     f.write(png)

# # Windows
# os.startfile("rag_graph.png")

# print("✅ Graph generated successfully")

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
from agentic_rag.evaluation_layer.evaluation_service import EvaluationService
from agentic_rag.query_layer.agents.query_decomposer import QueryDecomposer


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
evaluator = EvaluationService()
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
    

    result = memory_agent.run(state)

    
    return result


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
# def executor_node(state):

#     print("\n🧠 EXECUTOR NODE")

#     result = executor.run(
#         state["query"],
#         state["docs"],
#         state.get("chat_history")
#     )

#     # ------------------------------
#     # FIX: unpack executor output
#     # ------------------------------
#     state["answer"] = result.get("answer", "")
#     state["retrieval_failed"] = result.get("retrieval_failed", False)

#     print("📤 Answer:", state["answer"])
#     print("⚠ Retrieval Failed:", state["retrieval_failed"])

#     return state
def executor_node(state):

    print("\n🧠 EXECUTOR NODE")

    result = executor.run(
        state.get("query", ""),
        state.get("docs", []),
        state.get("chat_history", [])
    )

    if not isinstance(result, dict):
        result = {}

    state["answer"] = result.get("answer", "")
    state["retrieval_failed"] = result.get("retrieval_failed", False)

    print("📤 Answer:", state["answer"])
    print("⚠ Retrieval Failed:", state["retrieval_failed"])

    return state


@traceable(name="reasoning_node")
def reasoning_node(state):
    

    print("\n🧠 REASONING NODE")

    iteration = state.get("iteration", 0)

    print(f"🔁 Current Iteration: {iteration}")

    if iteration > 0 and iteration <= len(ADAPTIVE_RETRIEVAL_ORDER):
        new_index = ADAPTIVE_RETRIEVAL_ORDER[iteration - 1]
        print(f"🔄 Switching Retrieval Strategy → {new_index}")
        state["index"] = new_index

    result = reasoning_graph.invoke(state)
    state.update(result)

    if state.get("valid", False) and state.get("evaluation", {}).get("trusted", False):
        print("✅ Answer validated AND trusted → stopping loop")
        state["retry"] = False
        return state

    if state.get("retry", False):
        next_iteration = iteration + 1
        state["iteration"] = next_iteration

        print(f"🔁 Next Iteration Prepared: {next_iteration}")

        if next_iteration >= MAX_RETRIES:
            print("🛑 Max retries reached → stopping loop")
            state["retry"] = False

   
    return state


@traceable(name="evaluation_node")

# def evaluation_node(state):

#     print("\n📊 EVALUATION NODE")

#     try:
#         docs = state.get("docs", [])
#         answer = state.get("answer", "")

#         print("📦 Docs passed to evaluation:", len(docs))

#         # ------------------------------
#         # HANDLE INVALID ANSWER
#         # ------------------------------
#         if "NOT_FOUND" in answer:
#             print("⚠ Invalid answer → skipping eval")

#             state["evaluation"] = {
#                 "trusted": False,
#                 "reason": "invalid_answer"
#             }
#             return state

#         # ------------------------------
#         # RUN EVAL
#         # ------------------------------
#         result = evaluator.run(
#             state["query"],
#             answer,
#             docs
#         )

#         if not result:
#             result = {
#                 "trusted": False,
#                 "reason": "empty_eval"
#             }

#         state["evaluation"] = result

#         print("📊 Evaluation Result:", result)

#     except Exception as e:
#         print("⚠ Evaluation failed:", e)

#         state["evaluation"] = {
#             "trusted": False,
#             "reason": "evaluation_error",
#             "error": str(e)
#         }

#     return state
def evaluation_node(state):

    print("\n📊 EVALUATION NODE")

    try:
        raw_docs = state.get("docs", [])
        answer = state.get("answer", "")

        # ✅ normalize docs
        docs = []
        for d in raw_docs:
            try:
                docs.append(d.content)
            except:
                docs.append(str(d))

        print("📦 Docs passed to evaluation:", len(docs))

        # ✅ don't skip eval
        if "NOT_FOUND" in answer:
            print("⚠ Invalid answer → running eval with fallback context")
            docs = ["no relevant context"]

        # ✅ run eval
        result = evaluator.run(
            state.get("query", ""),
            answer,
            docs
        )

        if not result:
            print("⚠ Evaluator returned empty result")
            result = {
                "trusted": False,
                "reason": "empty_eval",
                "metrics": {}
            }

        state["evaluation"] = result

        print("📊 Evaluation Result:", result)

    except Exception as e:
        print("⚠ Evaluation failed:", e)

        state["evaluation"] = {
            "trusted": False,
            "reason": "evaluation_error",
            "error": str(e)
        }

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
builder.add_node("evaluation", evaluation_node)

builder.set_entry_point("guardrail")


# ------------------------------
# CONDITIONAL EDGES
# ------------------------------

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





def reasoning_router(state):

    # iteration = state.get("iteration", 0)
    # retry = state.get("retry", False)

    # print("\n🔹 Reasoning Router")
    # print("Iteration:", iteration)
    # print("Retry:", retry)

    # if iteration >= MAX_RETRIES:
    #     print("❌ Max retries reached → evaluation")
    #     return "evaluation"

    # if retry:
    #     print("🔁 Retry with next retrieval strategy")
    #     return "retry"

    # print("✅ Answer accepted → evaluation")
    # return "evaluation"
    

    iteration = state.get("iteration", 0)
    retry = state.get("retry", False)

    print("\n🔹 Reasoning Router")
    print("Iteration:", iteration)
    print("Retry:", retry)

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
    "retry": "controller",
    "end": END
}
)

builder.add_edge("rewrite", "memory")
builder.add_edge("plan", "decompose")
builder.add_edge("decompose", "select_index")
builder.add_edge("select_index", "controller")
builder.add_edge("controller", "retrieve")
builder.add_edge("retrieve", "execute")
# builder.add_edge("execute", "reason")
builder.add_edge("execute", "evaluation")
builder.add_edge("evaluation", "reason")




rag_graph = builder.compile()


# # ------------------------------
# # GRAPH IMAGE
# # ------------------------------

# from IPython.display import Image
# import os

# print("🎯 Generating RAG Graph Image...")

# png = rag_graph.get_graph().draw_mermaid_png()

# with open("rag_graph.png", "wb") as f:
#     f.write(png)

# os.startfile("rag_graph.png")

# print("✅ Graph generated successfully")