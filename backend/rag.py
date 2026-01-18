import httpx
from bs4 import BeautifulSoup
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
import re


model = SentenceTransformer("all-MiniLM-L6-v2")


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


def embed_texts(texts: List[str]) -> np.ndarray:
    return model.encode(texts, convert_to_numpy=True).astype("float32")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))




def generate_answer_simple(question: str, contexts: List[str]) -> str:
    if not contexts:
        return "I don't have enough information in the saved content to answer this."

    q = question.lower().strip()
    combined = " ".join(contexts)

   
    if "cgpa" in q:
        # find patterns like 8.46, 7.9, 9.1
        match = re.search(r"\b\d{1}\.\d{1,2}\b", combined)
        if match:
            return match.group(0)
        return "I don't have enough information in the saved content to answer this."

   
    if "percentage" in q or "%" in q:
        match = re.search(r"\b\d{1,2}\.?\d{0,2}\s?%\b", combined)
        if match:
            return match.group(0).replace(" ", "")
        return "I don't have enough information in the saved content to answer this."

   
    sentences = re.split(r'(?<=[.!?])\s+', combined.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 15]


    q_words = set(re.findall(r"[a-zA-Z0-9]+", q))
    best_sentence = None
    best_score = 0

    for s in sentences:
        s_words = set(re.findall(r"[a-zA-Z0-9]+", s.lower()))
        score = len(q_words.intersection(s_words))
        if score > best_score:
            best_score = score
            best_sentence = s

    if not best_sentence or best_score == 0:
        return "I don't have enough information in the saved content to answer this."

    return best_sentence