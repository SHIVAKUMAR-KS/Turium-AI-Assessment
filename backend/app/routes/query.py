"""
Query endpoint for RAG
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from typing import List, Dict

from app.database import get_content_item, content_item_to_dict
from app.embeddings import generate_embedding
from app.vector_store import search_similar
from app.llm import generate_answer
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


class QueryRequest(BaseModel):
    """Request model for query"""
    question: str


class SourceChunk(BaseModel):
    """Source chunk information"""
    content: str
    content_id: str
    source_type: str
    source_url: str | None


class QueryResponse(BaseModel):
    """Response model for query"""
    answer: str
    sources: List[SourceChunk]


@router.post("/query", response_model=QueryResponse)
async def query_knowledge(request: QueryRequest):
    """
    Query the knowledge base using RAG
    
    - **question**: User's question
    
    Returns answer with cited sources
    """
    try:
        if not request.question or not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )
        
        question = request.question.strip()
        logger.info(f"Processing query: {question}")
        
        # Generate query embedding
        query_embedding = generate_embedding(question)
        
        # Search for similar chunks
        similar_chunks = search_similar(
            query_embedding,
            n_results=settings.max_chunks_per_query
        )
        
        if not similar_chunks:
            return QueryResponse(
                answer="I couldn't find any relevant information in the knowledge base to answer your question.",
                sources=[]
            )
        
        logger.info(f"Found {len(similar_chunks)} relevant chunks")
        
        # Get full content items for source information
        content_ids = set(
            chunk['metadata']['content_id']  # Already string from MongoDB
            for chunk in similar_chunks
        )
        
        # Fetch content items from MongoDB
        content_items = {}
        for content_id in content_ids:
            item = await get_content_item(content_id)
            if item:
                content_items[content_id] = item
        
        # Format sources
        sources = []
        for chunk in similar_chunks:
            content_id = chunk['metadata']['content_id']
            content_item = content_items.get(content_id)
            
            if content_item:
                item_dict = content_item_to_dict(content_item)
                sources.append(SourceChunk(
                    content=chunk['document'],
                    content_id=content_id,
                    source_type=chunk['metadata']['source_type'],
                    source_url=item_dict.get('source_url')
                ))
        
        # Generate answer using RAG
        answer = generate_answer(question, similar_chunks)
        
        logger.info(f"Generated answer for query")
        
        return QueryResponse(
            answer=answer,
            sources=sources
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing query"
        )
