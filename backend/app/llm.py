"""
LLM integration for RAG queries
"""
from openai import OpenAI
import logging
from typing import List, Dict

from app.config import settings

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.openai_api_key)


def generate_answer(question: str, context_chunks: List[Dict]) -> str:
    """
    Generate answer using RAG pipeline
    
    Args:
        question: User's question
        context_chunks: List of relevant context chunks with metadata
        
    Returns:
        Generated answer string
    """
    # Format context from chunks
    context_text = "\n\n".join([
        f"[Source {i+1}]: {chunk['document']}"
        for i, chunk in enumerate(context_chunks)
    ])
    
    # Build prompt
    system_prompt = """You are a helpful assistant that answers questions based on the provided context.
If the context doesn't contain enough information to answer the question, say so.
Be concise and accurate. Cite which source(s) you used when relevant."""

    user_prompt = f"""Context:
{context_text}

Question: {question}

Answer based on the context above:"""

    try:
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        raise

