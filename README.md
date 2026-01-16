# AI Knowledge Inbox

A minimal production-style web application for knowledge management with RAG (Retrieval-Augmented Generation) capabilities.

## Features

- **Content Ingestion**: Save text notes or fetch content from URLs
- **Semantic Search**: Find relevant content using embeddings
- **RAG Queries**: Ask questions and get answers with source citations
- **Clean UI**: Simple, functional React interface

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite
- **AI**: OpenAI (embeddings + LLM)
- **Vector Store**: ChromaDB
- **Database**: SQLite

## Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database (see `backend/POSTGRES_SETUP.md` for details):
```bash
createdb knowledge_inbox
```

5. Create `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=knowledge_inbox
```

6. Run the server:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open http://localhost:3000 in your browser

## API Endpoints

- `POST /api/ingest` - Ingest text or URL content
  ```json
  {
    "content": "Your text note" // OR
    "url": "https://example.com"
  }
  ```

- `GET /api/items` - List all saved items

- `POST /api/query` - Query the knowledge base
  ```json
  {
    "question": "What is the main topic?"
  }
  ```

## Architecture Decisions

### Chunking Strategy
- **Approach**: Sentence-aware chunking with overlap
- **Rationale**: Preserves semantic meaning by keeping sentences intact
- **Config**: 500 chars per chunk, 50 char overlap (configurable)

### Vector Store
- **Choice**: ChromaDB (persistent, lightweight)
- **Rationale**: 
  - No external dependencies
  - Persistent storage
  - Simple API
  - Good for single-user/small-scale use

### Embeddings
- **Model**: OpenAI text-embedding-3-small
- **Rationale**: Good balance of quality and cost

### LLM
- **Model**: GPT-3.5-turbo
- **Rationale**: Cost-effective for RAG queries

### Database
- **Choice**: PostgreSQL
- **Rationale**: Production-ready, scalable, supports concurrent connections
- **Driver**: psycopg2-binary for SQLAlchemy integration

### Scale Considerations
- **Current**: Single-user, PostgreSQL + ChromaDB
- **At Scale**: 
  - Would need: PostgreSQL + pgvector (for vector search in DB), Redis cache, async task queue
  - Authentication/authorization
  - Rate limiting
  - Distributed vector store (Pinecone, Weaviate)
  - Background job processing for URL fetching

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── routes/       # API endpoints
│   │   ├── chunking.py   # Text chunking logic
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # SQLAlchemy models
│   │   ├── embeddings.py # OpenAI embeddings
│   │   ├── llm.py        # RAG query generation
│   │   ├── url_fetcher.py # URL content extraction
│   │   └── vector_store.py # ChromaDB integration
│   ├── main.py           # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main component
│   │   ├── main.jsx      # Entry point
│   │   └── index.css     # Styles
│   └── package.json
└── README.md
```

## Development Notes

- Structured logging throughout
- Error handling with appropriate HTTP status codes
- Input validation using Pydantic
- Clear separation of concerns
- No god files or copy-paste code

