# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from agentic_rag.api.chat_service import run_chat
# from agentic_rag.api.schemas import (
#     ChatRequest,
#     ChatResponse,
#     QueryRequest,
#     QueryResponse
# )

# from agentic_rag.query_layer.graph.rag_graph import rag_graph


# app = FastAPI(
#     title="Agentic RAG API",
#     version="1.0",
#     description="FastAPI service for Agentic RAG chatbot"
# )


# # ---------- CORS ----------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ---------- Health Check ----------
# @app.get("/")
# def health():
#     return {"status": "running"}


# # ---------- Chat Endpoint ----------
# @app.post("/chat", response_model=ChatResponse)
# async def chat(req: ChatRequest):

#     answer = run_chat(
#         req.session_id,
#         req.message
#     )

#     return ChatResponse(
#         answer=answer
#     )


# # ---------- Query Endpoint ----------
# @app.post("/query", response_model=QueryResponse)
# async def query(req: QueryRequest):

#     result = rag_graph.invoke({
#         "query": req.query
#     })

#     answer = result.get("answer", "")

#     docs = result.get("docs", [])

#     sources = []

#     for i, d in enumerate(docs[:5]):
#         try:
#             sources.append(d.content[:200])
#         except:
#             sources.append(str(d)[:200])

#     return QueryResponse(
#         answer=answer,
#         sources=sources
#     )

# 🔥 MUST BE FIRST (DO NOT MOVE)
from agentic_rag.langsmith_setup import init_langsmith


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langsmith import traceable
from agentic_rag.query_layer.graph.rag_executor import execute_rag_graph
from agentic_rag.api.chat_service import run_chat
from agentic_rag.api.schemas import (
    ChatRequest,
    ChatResponse,
    QueryRequest,
    QueryResponse
)

from agentic_rag.query_layer.graph.rag_graph import rag_graph

init_langsmith()
app = FastAPI(
    title="Agentic RAG API",
    version="1.0",
    description="FastAPI service for Agentic RAG chatbot"
)


# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Health ----------
@app.get("/")
def health():
    return {"status": "running"}


# 🔥 ROOT TRACE FOR CHAT (MOST IMPORTANT)
@traceable(name="api_chat_endpoint", run_type="chain")
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):

    answer = run_chat(
        req.session_id,
        req.message
    )

    return ChatResponse(answer=answer)


# 🔥 ROOT TRACE FOR QUERY
@traceable(name="api_query_endpoint", run_type="chain")
@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):

    state = {
        "query": req.query,
        "iteration": 0
    }

    result = execute_rag_graph(state)

    answer = result.get("answer", "")
    docs = result.get("docs", [])

    sources = []

    for d in docs[:5]:
        try:
            sources.append(d.content[:200])
        except:
            sources.append(str(d)[:200])

    return QueryResponse(
        answer=answer,
        sources=sources
    )