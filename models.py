from pydantic import BaseModel, HttpUrl
from typing import Optional, Literal, List


class IngestRequest(BaseModel):
    type: Literal["note", "url"]
    content: str  # note text OR URL string


class ItemResponse(BaseModel):
    id: str
    type: str
    content: str
    created_at: str


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3


class SourceChunk(BaseModel):
    item_id: str
    chunk: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
