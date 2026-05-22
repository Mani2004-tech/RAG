from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agentic_rag.api.chat_service import run_chat
from agentic_rag.api.schemas import ChatRequest, ChatResponse, QueryRequest, QueryResponse
from agentic_rag.query_layer.graph.rag_graph import rag_graph

app = FastAPI(
    title="Agentic RAG API",
    version="1.0",
    description="FastAPI service for Agentic RAG chatbot",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    answer = run_chat(req.session_id, req.message)
    return ChatResponse(answer=answer)


@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    result = rag_graph.invoke({"query": req.query})

    answer = result.get("answer", "")
    docs = result.get("docs", [])

    sources = []
    for d in docs[:5]:
        try:
            sources.append(d.content[:200])
        except Exception:
            sources.append(str(d)[:200])

    return QueryResponse(answer=answer, sources=sources)
