"""
Content ingestion endpoint
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl, model_validator
import logging
from typing import Optional

from app.database import create_content_item, ContentType
from app.chunking import chunk_text
from app.embeddings import generate_embeddings
from app.vector_store import add_embeddings
from app.url_fetcher import fetch_url_content
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


class IngestRequest(BaseModel):
    """Request model for content ingestion"""
    content: Optional[str] = None
    url: Optional[HttpUrl] = None
    
    @model_validator(mode='after')
    def validate_input(self):
        """Ensure either content or url is provided"""
        if not self.content and not self.url:
            raise ValueError("Either 'content' or 'url' must be provided")
        if self.content and self.url:
            raise ValueError("Provide either 'content' or 'url', not both")
        return self


class IngestResponse(BaseModel):
    """Response model for content ingestion"""
    id: str
    message: str
    chunks_count: int


@router.post("/ingest", response_model=IngestResponse, status_code=201)
async def ingest_content(request: IngestRequest):
    """
    Ingest content (text note or URL)
    
    - **content**: Plain text note
    - **url**: URL to fetch and process
    """
    try:
        # Determine content and source type
        if request.url:
            # Fetch URL content
            logger.info(f"Fetching content from URL: {request.url}")
            content_text = await fetch_url_content(str(request.url))
            
            if not content_text:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to fetch content from URL"
                )
            
            source_type = ContentType.URL
            source_url = str(request.url)
            content = content_text
        else:
            # Use provided text content
            if not request.content or not request.content.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Content cannot be empty"
                )
            
            source_type = ContentType.TEXT
            source_url = None
            content = request.content.strip()
        
        # Store in MongoDB
        db_item = await create_content_item(
            content=content,
            source_type=source_type,
            source_url=source_url
        )
        
        item_id = str(db_item["_id"])
        logger.info(f"Stored content item {item_id} ({source_type})")
        
        # Chunk the content
        chunks = chunk_text(content)
        logger.info(f"Created {len(chunks)} chunks for item {item_id}")
        
        # Generate embeddings
        embeddings = generate_embeddings(chunks)
        
        # Prepare metadata for each chunk
        metadatas = [
            {
                "content_id": item_id,  # Use string ID for MongoDB
                "source_type": source_type,
                "source_url": source_url,
                "chunk_index": i
            }
            for i in range(len(chunks))
        ]
        
        # Store embeddings
        add_embeddings(
            content_id=item_id,  # Pass as string
            chunks=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        logger.info(f"Stored embeddings for item {item_id}")
        
        return IngestResponse(
            id=item_id,
            message="Content ingested successfully",
            chunks_count=len(chunks)
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error ingesting content: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while ingesting content"
        )
