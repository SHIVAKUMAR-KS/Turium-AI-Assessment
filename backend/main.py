from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import numpy as np

from models import IngestRequest, QueryRequest
from db import init_db, get_conn
from rag import chunk_text, fetch_url_text, embed_texts, cosine_similarity, generate_answer_simple

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home():
    return {"message": "AI Knowledge Inbox API running (SQLite + Local Embeddings) 🚀"}


@app.post("/ingest")
async def ingest(req: IngestRequest):
    try:
        raw_text = req.content

        if req.type == "url":
            raw_text = await fetch_url_text(req.content)

        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="Content is empty")

        created_at = datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()
        conn = get_conn()
        cur = conn.cursor()

        # Insert item
        cur.execute(
            "INSERT INTO items (type, content, raw_text, created_at) VALUES (?, ?, ?, ?)",
            (req.type, req.content, raw_text, created_at),
        )
        item_id = cur.lastrowid

        # Chunk + embed
        chunks = chunk_text(raw_text)
        if len(chunks) == 0:
            raise HTTPException(status_code=400, detail="No chunkable content found")

        embeddings = embed_texts(chunks)

        for i, (ch, emb) in enumerate(zip(chunks, embeddings)):
            cur.execute(
                "INSERT INTO chunks (item_id, chunk_index, chunk, embedding, created_at) VALUES (?, ?, ?, ?, ?)",
                (item_id, i, ch, json.dumps(emb.tolist()), created_at),
            )

        conn.commit()
        conn.close()

        return {"message": "Ingested successfully", "item_id": item_id, "chunks": len(chunks)}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingest failed: {str(e)}")


@app.get("/items")
def get_items():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, type, content, created_at FROM items ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()

    items = []
    for r in rows:
        items.append({
            "id": r["id"],
            "type": r["type"],
            "content": r["content"],
            "created_at": r["created_at"]
        })

    return items


@app.post("/query")
def query(req: QueryRequest):
    try:
        question = req.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")

        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT item_id, chunk, embedding FROM chunks")
        rows = cur.fetchall()
        conn.close()

        if len(rows) == 0:
            raise HTTPException(status_code=400, detail="No data found. Please ingest notes/urls first.")

        q_emb = embed_texts([question])[0]

        scored = []
        for r in rows:
            emb = np.array(json.loads(r["embedding"]), dtype=np.float32)
            score = cosine_similarity(q_emb, emb)
            scored.append({
                "item_id": r["item_id"],
                "chunk": r["chunk"],
                "score": float(score)
            })

        scored.sort(key=lambda x: x["score"], reverse=True)

        # safer top_k (avoid huge context)
        top_k = min(max(req.top_k, 1), 5)
        top_chunks = scored[:top_k]

        contexts = []
        for x in top_chunks:
            c = x["chunk"].strip()
            # limit chunk size
            if len(c) > 800:
                c = c[:800] + "..."
            contexts.append(c)

        answer = generate_answer_simple(question, contexts)

        # return sources as snippets only
        sources = []
        for x in top_chunks:
            snippet = x["chunk"].strip()
            if len(snippet) > 220:
                snippet = snippet[:220] + "..."

            sources.append({
                "item_id": x["item_id"],
                "score": x["score"],
                "snippet": snippet
            })

        return {"answer": answer, "sources": sources}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")



    try:
        question = req.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")

        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT item_id, chunk, embedding FROM chunks")
        rows = cur.fetchall()
        conn.close()

        if len(rows) == 0:
            raise HTTPException(status_code=400, detail="No data found. Please ingest notes/urls first.")

        q_emb = embed_texts([question])[0]

        scored = []
        for r in rows:
            emb = np.array(json.loads(r["embedding"]), dtype=np.float32)
            score = cosine_similarity(q_emb, emb)
            scored.append({
                "item_id": r["item_id"],
                "chunk": r["chunk"],
                "score": score
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        top_chunks = scored[:req.top_k]

        contexts = [x["chunk"] for x in top_chunks]
        answer = generate_answer_simple(question, contexts)

        return {"answer": answer, "sources": top_chunks}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
