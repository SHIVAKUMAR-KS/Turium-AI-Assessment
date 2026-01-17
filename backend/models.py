from pydantic import BaseModel
from typing import Literal


class IngestRequest(BaseModel):
    type: Literal["note", "url"]
    content: str


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3
