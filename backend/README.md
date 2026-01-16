# AI Knowledge Inbox - Backend

FastAPI backend for the AI Knowledge Inbox application.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up MongoDB (see `MONGODB_SETUP.md` for details):

```bash
# Ensure MongoDB is running
# No database creation needed - MongoDB creates it automatically
```

3. Create `.env` file:

```bash
# Edit .env and add:
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB=knowledge_inbox
```

4. Run the server:

```bash
uvicorn main:app --reload --port 8000
```

## API Endpoints

- `POST /api/ingest` - Ingest text or URL content
- `GET /api/items` - List all saved items
- `POST /api/query` - Query the knowledge base

## Architecture Decisions

- **Vector Store**: ChromaDB for persistent vector storage
- **Chunking**: Sentence-aware chunking with configurable overlap
- **Embeddings**: OpenAI text-embedding-3-small
- **LLM**: GPT-3.5-turbo for RAG queries
- **Database**: MongoDB for content metadata
