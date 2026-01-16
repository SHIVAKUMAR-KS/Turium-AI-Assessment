"""
Vector store for embeddings using ChromaDB
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
import os
from typing import List, Dict, Optional

from app.config import settings

# Initialize ChromaDB client
os.makedirs(settings.chroma_db_path, exist_ok=True)
chroma_client = chromadb.PersistentClient(
    path=settings.chroma_db_path,
    settings=ChromaSettings(anonymized_telemetry=False)
)

# Get or create collection
collection = chroma_client.get_or_create_collection(
    name="knowledge_embeddings",
    metadata={"description": "Embeddings for knowledge inbox content chunks"}
)


def add_embeddings(
    content_id: str,  # Changed to str for MongoDB ObjectId
    chunks: List[str],
    embeddings: List[List[float]],
    metadatas: List[Dict]
):
    """
    Add embeddings to vector store
    
    Args:
        content_id: ID of the content item (string for MongoDB)
        chunks: List of text chunks
        embeddings: List of embedding vectors
        metadatas: List of metadata dicts for each chunk
    """
    ids = [f"{content_id}_{i}" for i in range(len(chunks))]
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )


def search_similar(
    query_embedding: List[float],
    n_results: int = 5
) -> List[Dict]:
    """
    Search for similar content chunks
    
    Args:
        query_embedding: Query embedding vector
        n_results: Number of results to return
        
    Returns:
        List of dicts with 'document', 'metadata', 'distance'
    """
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # Format results
    formatted_results = []
    if results['documents'] and len(results['documents'][0]) > 0:
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                "document": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "distance": results['distances'][0][i] if results['distances'] else None
            })
    
    return formatted_results


def delete_content_embeddings(content_id: str):
    """Delete all embeddings for a content item"""
    # Get all IDs for this content_id
    results = collection.get()
    ids_to_delete = [
        id for id in results['ids']
        if id.startswith(f"{content_id}_")
    ]
    
    if ids_to_delete:
        collection.delete(ids=ids_to_delete)

