"""
OpenAI embeddings generation
"""
from typing import List
from openai import OpenAI
import logging

from app.config import settings

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.openai_api_key)


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts
    
    Args:
        texts: List of text strings
        
    Returns:
        List of embedding vectors
    """
    try:
        response = client.embeddings.create(
            model=settings.embedding_model,
            input=texts
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text
    
    Args:
        text: Text string
        
    Returns:
        Embedding vector
    """
    return generate_embeddings([text])[0]

