from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from models import IngestRequest, QueryRequest
from db import items_collection
from rag import chunk_text, fetch_url_text, add_chunks, search_chunks, generate_answer_simple


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Knowledge Inbox API running (LOCAL RAG) 🚀"}


@app.post("/ingest")
async def ingest(req: IngestRequest):
    try:
        raw_text = req.content

        if req.type == "url":
            raw_text = await fetch_url_text(req.content)

        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="Content is empty")

        item_doc = {
            "type": req.type,
            "content": req.content,
            "raw_text": raw_text,
            "created_at": datetime.utcnow().isoformat()
        }
        result = items_collection.insert_one(item_doc)
        item_id = str(result.inserted_id)

        chunks = chunk_text(raw_text)
        if len(chunks) == 0:
            raise HTTPException(status_code=400, detail="No chunkable content found")

        # store into FAISS local index
        add_chunks(item_id, chunks)


        return {"message": "Ingested successfully", "item_id": item_id, "chunks": len(chunks)}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingest failed: {str(e)}")


@app.get("/items")
def get_items():
    items = []
    for item in items_collection.find().sort("created_at", -1):
        items.append({
            "id": str(item["_id"]),
            "type": item["type"],
            "content": item["content"],
            "created_at": item["created_at"]
        })
    return items


@app.post("/query")
def query(req: QueryRequest):
    try:
        question = req.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")

        results = search_chunks(question, req.top_k)
        contexts = [r["chunk"] for r in results]

        answer = generate_answer_simple(question, contexts)

        return {"answer": answer, "sources": results}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
