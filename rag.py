import httpx
from bs4 import BeautifulSoup
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

chunk_store = []  # each: {"item_id":..., "chunk":..., "embedding":...}


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)

    return chunks


async def fetch_url_text(url: str) -> str:
    async with httpx.AsyncClient(timeout=15) as client_http:
        r = await client_http.get(url)
        r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(separator=" ", strip=True)
    return text[:12000]


def add_chunks(item_id: str, chunks: List[str]):
    embeddings = model.encode(chunks, convert_to_numpy=True).astype("float32")

    for ch, emb in zip(chunks, embeddings):
        chunk_store.append({
            "item_id": item_id,
            "chunk": ch,
            "embedding": emb
        })


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def search_chunks(question: str, top_k: int = 3):
    if len(chunk_store) == 0:
        return []

    q_emb = model.encode([question], convert_to_numpy=True)[0].astype("float32")

    scored = []
    for obj in chunk_store:
        score = cosine_similarity(q_emb, obj["embedding"])
        scored.append({
            "item_id": obj["item_id"],
            "chunk": obj["chunk"],
            "score": score
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def generate_answer_simple(question: str, contexts: List[str]) -> str:
    if not contexts:
        return "I don't have enough information in your saved inbox."

    return f"""
Answer (based on your saved inbox context):
{contexts[0]}

Question:
{question}
""".strip()
