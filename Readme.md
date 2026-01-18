# 📌 AI Knowledge Inbox (Minimal RAG App)

A minimal production-style web app that allows users to:

✅ Save short notes or URLs  
✅ Fetch and store URL content server-side  
✅ Ask questions over saved content using semantic search + RAG  
✅ Get answers with cited source chunks  

Built as an interview task focusing on **frontend + backend + async ingestion + AI integration + system design** without overengineering.

---

## 🚀 Features

### 1) Content Ingestion
- Add **plain text notes**
- Add **URLs**
  - Fetches web page content **server-side**
  - Extracts readable text using HTML parsing
- Stores:
  - raw content (`raw_text`)
  - metadata (`created_at`, `type`)

### 2) Semantic Search + RAG
- **Chunking**: fixed-size chunking with overlap (intentional for context continuity)
- **Embeddings**: local embeddings using `sentence-transformers`
- **Vector Store**: lightweight SQLite storage (embeddings stored per chunk)
- **Retrieval**: cosine similarity + top_k chunk selection
- **RAG Response**:
  - Returns answer + cited source chunks

### 3) Frontend (React)
- Add note / URL input
- List saved items
- Ask question interface
- Display answer + retrieved sources/snippets

---

## 🧱 Tech Stack

### Backend
- FastAPI (Python)
- SQLite (lightweight DB)
- SentenceTransformers (local embeddings)
- Semantic search using cosine similarity
- HTTPX + BeautifulSoup (server-side URL fetching and parsing)

### Frontend
- React (Hooks)
- Axios

---

## 📁 Project Structure

```txt
ai-knowledge-inbox/
│── backend/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── rag.py
│   ├── inbox.db            ## 📌 AI Knowledge Inbox (Minimal RAG App)

AI Knowledge Inbox is a minimal, production-style web app that allows users to:

✅ Save short notes or URLs  
✅ Fetch and store URL content server-side  
✅ Ask questions over saved content using semantic search + a simple RAG pipeline  
✅ Get short, relevant answers + source snippets with similarity scores  

Built as an interview assignment focusing on **frontend + backend + ingestion + embeddings + retrieval + system design** without overengineering.

---

## 🚀 Features

 1) Content Ingestion
- Add plain text notes**
- Add URLs
  - Fetches web page content server-side
  - Extracts readable text using HTML parsing (BeautifulSoup)
- Stores:
  - raw content (`raw_text`)
  - metadata (`created_at`, `type`)

---

 2) Semantic Search + RAG (Minimal)
This project implements a lightweight RAG flow:

- Chunking: fixed-size chunking with overlap (to preserve context continuity)
- Embeddings: local embeddings using `sentence-transformers` (`all-MiniLM-L6-v2`)
- Vector Store: SQLite table storing embeddings per chunk (JSON)
- Retrieval:
  - cosine similarity scoring
  - top_k chunk selection (default 3)
- Answering:
  - Generates a short answer instead of returning full stored content
  - Supports exact-value extraction for questions like CGPA / percentage
  - Uses a relevance gate to avoid answering unrelated questions

---

 3) Frontend (React)
- Add note / URL input
- List saved items
- Ask question interface
- Display:
  - final answer
  - retrieved source snippets + similarity scores

---

## 🧱 Tech Stack

 Backend
- FastAPI (Python)
- SQLite (lightweight DB)
- SentenceTransformers (local embeddings)
- Semantic search using cosine similarity
- HTTPX + BeautifulSoup (server-side URL fetching + parsing)

 Frontend
- React (Hooks)
- Axios
- Minimal UI with tabs (Add Content / Saved Items / Ask Question)

---

  Project Structure
```txt
ai-knowledge-inbox/
│── backend/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── rag.py
│   ├── inbox.db            # auto-created
│   ├── requirements.txt
│
│── frontend/
│   ├── src/App.jsx
│   ├── src/index.css
│   ├── package.json
```

---

## ⚙️ Setup Instructions

### ✅ 1) Backend Setup (FastAPI)

Go to backend folder:
```bash
cd backend
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run backend:
```bash
uvicorn main:app --reload
```

Backend runs at: 📍 **http://127.0.0.1:8000**

---

### ✅ 2) Frontend Setup (React + Vite)

Go to frontend folder:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Run frontend:
```bash
npm run dev
```

Frontend runs at: 📍 **http://localhost:3000**

---

## 🔌 API Endpoints

### 1) Health Check

**GET** `/`

**Response:**
```json
{
  "message": "AI Knowledge Inbox API running (SQLite + Local Embeddings) 🚀"
}
```

---

### 2) Ingest Note / URL

**POST** `/ingest`

#### Add Note

**Body:**
```json
{
  "type": "note",
  "content": "FastAPI is a Python framework for building APIs."
}
```

#### Add URL

**Body:**
```json
{
  "type": "url",
  "content": "https://example.com"
}
```

**Response:**
```json
{
  "message": "Ingested successfully",
  "item_id": 1,
  "chunks": 4
}
```

---

### 3) List Saved Items

**GET** `/items`

**Response:**
```json
[
  {
    "id": 1,
    "type": "note",
    "content": "FastAPI is a Python framework...",
    "created_at": "2026-01-17T12:30:00.000Z"
  }
]
```

---

### 4) Ask Question (RAG Query)

**POST** `/query`

**Body:**
```json
{
  "question": "What is FastAPI used for?",
  "top_k": 3
}
```

**Response:**
```json
{
  "answer": "FastAPI is used to build APIs quickly with Python.",
  "sources": [
    {
      "item_id": 1,
      "score": 0.82,
      "snippet": "FastAPI is a modern Python framework used to build APIs..."
    }
  ]
}
```

---

## 🧠 RAG Design Notes (Tradeoffs)

### Chunking Strategy

- Fixed chunk size with overlap to preserve context across chunk boundaries
- Simple and intentional for small-scale ingestion

### Embeddings

- Uses local SentenceTransformers model: **all-MiniLM-L6-v2**
- No external API key required

### Retrieval + Relevance Gate

- Retrieval is done using cosine similarity
- A similarity threshold can be used to prevent irrelevant answers:
  - If best similarity score is too low → return:  
    `"I don't have enough information in the saved content to answer this."`

### Answer Quality

Instead of returning entire chunks, the app returns:

- **short answers** (sentence-level)
- **exact-value extraction** for specific queries like CGPA/percentage

This makes the response more user-friendly and closer to real RAG behavior.

### What breaks at scale?

- Retrieval is currently **O(N)** across all stored chunks
- SQLite is suitable for minimal use but not optimized for large-scale vector search

### Production Improvements (Future Work)

Replace brute-force similarity scan with:

- **FAISS** (local)
- **pgvector** (Postgres)
- **Qdrant / Pinecone / Weaviate**

Add async background jobs for ingestion

Add caching and pagination for items

Add authentication + multi-user support

Add structured citations like `[1]` `[2]`

Add monitoring/logging + rate limits

---

## 🧪 Testing with Postman

### Ingest Note

**POST** `http://127.0.0.1:8000/ingest`
```json
{
  "type": "note",
  "content": "FastAPI is used to build APIs quickly."
}
```

### Get Items

**GET** `http://127.0.0.1:8000/items`

### Ask Question

**POST** `http://127.0.0.1:8000/query`
```json
{
  "question": "What is FastAPI used for?",
  "top_k": 3
}
```

---

## 🗄️ View SQLite Data

The database file is created automatically:

📌 **backend/inbox.db**

You can inspect it using:

- **DB Browser for SQLite**
- OR **sqlite3 CLI**

### Example SQL:
```sql
SELECT * FROM items;
SELECT * FROM chunks LIMIT 5;
```



If you want, I can also generate a final polished README with:
✅ screenshots section  
✅ API request/response examples for both note + URL  
✅ known issues section (like snippet display fix)  
✅ deployment section (Docker optional) auto-created
│   ├── requirements.txt
│
│── frontend/
│   ├── src/App.jsx
│   ├── src/index.css
│   ├── package.json
```
# ⚙️ Setup Instructions

## ✅ 1) Backend Setup (FastAPI)

Go to backend folder:
```bash
cd backend
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run backend:
```bash
uvicorn main:app --reload
```

Backend runs at: 📍 **http://127.0.0.1:8000**

---

## ✅ 2) Frontend Setup (React)

Go to frontend folder:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Run frontend:
```bash
npm start
```

Frontend runs at: 📍 **http://localhost:3000**

---

# 🔌 API Endpoints

## 1) Health Check

**GET** `/`

**Response:**
```json
{
  "message": "AI Knowledge Inbox API running (SQLite + Local Embeddings) 🚀"
}
```

---

## 2) Ingest Note / URL

**POST** `/ingest`

### Add Note

**Body:**
```json
{
  "type": "note",
  "content": "FastAPI is a Python framework for building APIs."
}
```

### Add URL

**Body:**
```json
{
  "type": "url",
  "content": "https://example.com"
}
```

**Response:**
```json
{
  "message": "Ingested successfully",
  "item_id": 1,
  "chunks": 4
}
```

---

## 3) List Saved Items

**GET** `/items`

**Response:**
```json
[
  {
    "id": 1,
    "type": "note",
    "content": "FastAPI is a Python framework...",
    "created_at": "2026-01-17T12:30:00.000Z"
  }
]
```

---

## 4) Ask Question (RAG Query)

**POST** `/query`

**Body:**
```json
{
  "question": "What is FastAPI used for?",
  "top_k": 3
}
```

**Response:**
```json
{
  "answer": "FastAPI is used to build APIs quickly with Python...",
  "sources": [
    {
      "item_id": 1,
      "chunk": "FastAPI is a modern Python framework...",
      "score": 0.82
    }
  ]
}
```

---

# 🧠 RAG Design Notes (Tradeoffs)

## Chunking Strategy
- Fixed chunk size with overlap to preserve context across boundaries
- Simple and intentional for small-scale ingestion

## Embeddings
- Uses local sentence-transformers model: **all-MiniLM-L6-v2**
- No external API required

## Vector Storage
- Embeddings stored in SQLite as JSON per chunk
- Retrieval runs by loading embeddings and computing cosine similarity

## What breaks at scale?
- Retrieval is currently **O(N)** across all chunks → slow for large datasets
- SQLite is good for minimal use, but not optimized for large-scale vector search

## Production improvements
- Replace similarity scan with:
  - **FAISS** (local)
  - **pgvector** (Postgres)
  - **Qdrant / Pinecone / Weaviate**
- Add async background jobs for ingestion
- Add caching and pagination for items
- Add monitoring/logging and rate limits

---

# 🧪 Testing with Postman

## Ingest Note

**POST** `http://127.0.0.1:8000/ingest`
```json
{
  "type": "note",
  "content": "FastAPI is used to build APIs quickly."
}
```

## Get Items

**GET** `http://127.0.0.1:8000/items`

## Ask Question

**POST** `http://127.0.0.1:8000/query`
```json
{
  "question": "What is FastAPI used for?",
  "top_k": 3
}
```

---

# 🗄️ View SQLite Data

The database file is created automatically:

📌 **backend/inbox.db**

You can inspect it using:
- **DB Browser for SQLite**
- OR using Python / sqlite3 CLI

### Example SQL:
```sql
SELECT * FROM items;
SELECT * FROM chunks LIMIT 5;
```

---

# 👤 Author

**Shiva Kumar**  
Minimal AI Knowledge Inbox (RAG) – Interview Task Project