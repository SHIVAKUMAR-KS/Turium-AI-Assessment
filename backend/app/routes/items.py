"""
Items listing endpoint
"""
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

from app.database import get_all_content_items, content_item_to_dict

router = APIRouter()


class ItemResponse(BaseModel):
    """Response model for content item"""
    id: str
    content: str
    source_type: str
    source_url: str | None
    metadata: str | None
    created_at: str


@router.get("/items", response_model=List[ItemResponse])
async def get_items():
    """
    Get all saved content items
    
    Returns list of all ingested content items
    """
    items = await get_all_content_items()
    return [ItemResponse(**content_item_to_dict(item)) for item in items]
