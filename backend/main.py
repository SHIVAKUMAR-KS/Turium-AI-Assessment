"""
AI Knowledge Inbox - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from app.routes import ingest, items, query
from app.database import init_db, close_db

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup on startup/shutdown"""
    logger.info("Initializing database and vector store...")
    init_db()
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown")
    await close_db()


app = FastAPI(
    title="AI Knowledge Inbox API",
    description="RAG-powered knowledge management system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(ingest.router, prefix="/api", tags=["ingest"])
app.include_router(items.router, prefix="/api", tags=["items"])
app.include_router(query.router, prefix="/api", tags=["query"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "AI Knowledge Inbox API"}


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "ai-knowledge-inbox"
    }

