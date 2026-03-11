from pydantic import BaseModel
from typing import List, Optional


# -------- Chat Schemas --------

class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    answer: str


# -------- Query Schemas (single-shot RAG) --------

class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = []