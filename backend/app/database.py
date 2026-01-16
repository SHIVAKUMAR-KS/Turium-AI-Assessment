"""
Database models and initialization - MongoDB
"""
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import Optional
from bson import ObjectId
import logging

from app.config import settings

logger = logging.getLogger(__name__)

# MongoDB client
client: Optional[AsyncIOMotorClient] = None
database = None


def get_database():
    """Get MongoDB database instance"""
    global database
    if database is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return database


def init_db():
    """Initialize MongoDB connection"""
    global client, database
    try:
        mongodb_url = settings.get_mongodb_url
        logger.info(f"Connecting to MongoDB: {mongodb_url.split('@')[-1] if '@' in mongodb_url else mongodb_url}")
        
        client = AsyncIOMotorClient(mongodb_url)
        database = client[settings.mongodb_db]
        
        # Test connection
        # Note: We can't use async here, so we'll test on first use
        logger.info("MongoDB connection initialized")
        
    except Exception as e:
        logger.error(f"Error initializing MongoDB: {e}")
        raise


async def close_db():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")


# Content type enum values
class ContentType:
    TEXT = "text"
    URL = "url"


# Collection name
CONTENT_ITEMS_COLLECTION = "content_items"


async def create_content_item(content: str, source_type: str, source_url: Optional[str] = None, item_metadata: Optional[str] = None) -> dict:
    """
    Create a new content item in MongoDB
    
    Returns:
        dict with inserted_id
    """
    db = get_database()
    collection = db[CONTENT_ITEMS_COLLECTION]
    
    item = {
        "content": content,
        "source_type": source_type,
        "source_url": source_url,
        "metadata": item_metadata,
        "created_at": datetime.utcnow()
    }
    
    result = await collection.insert_one(item)
    item["_id"] = result.inserted_id
    return item


async def get_content_item(item_id: str) -> Optional[dict]:
    """Get a content item by ID"""
    db = get_database()
    collection = db[CONTENT_ITEMS_COLLECTION]
    
    try:
        item = await collection.find_one({"_id": ObjectId(item_id)})
        return item
    except Exception:
        return None


async def get_all_content_items() -> list:
    """Get all content items, sorted by created_at descending"""
    db = get_database()
    collection = db[CONTENT_ITEMS_COLLECTION]
    
    cursor = collection.find().sort("created_at", -1)
    items = await cursor.to_list(length=None)
    
    # Convert ObjectId to string for JSON serialization
    for item in items:
        item["id"] = str(item["_id"])
        del item["_id"]
    
    return items


def content_item_to_dict(item: dict) -> dict:
    """Convert MongoDB document to API response format"""
    return {
        "id": str(item.get("_id", item.get("id"))),
        "content": item.get("content", ""),
        "source_type": item.get("source_type", ""),
        "source_url": item.get("source_url"),
        "metadata": item.get("metadata"),
        "created_at": item.get("created_at").isoformat() if item.get("created_at") else None
    }
