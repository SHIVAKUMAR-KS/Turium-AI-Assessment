"""
Text chunking strategy
Simple sentence-aware chunking with overlap
"""
import re
from typing import List

from app.config import settings


def chunk_text(text: str, chunk_size: int = None, chunk_overlap: int = None) -> List[str]:
    """
    Chunk text into smaller pieces with overlap
    
    Strategy:
    - Split on sentence boundaries (., !, ?)
    - Respect chunk_size and chunk_overlap
    - Prefer keeping sentences intact
    
    Args:
        text: Text to chunk
        chunk_size: Maximum characters per chunk
        chunk_overlap: Characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    chunk_size = chunk_size or settings.chunk_size
    chunk_overlap = chunk_overlap or settings.chunk_overlap
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        sentence_length = len(sentence)
        
        # If adding this sentence would exceed chunk_size, finalize current chunk
        if current_length + sentence_length > chunk_size and current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append(chunk_text)
            
            # Start new chunk with overlap
            if chunk_overlap > 0:
                # Take last few sentences for overlap
                overlap_text = ' '.join(current_chunk[-2:]) if len(current_chunk) >= 2 else current_chunk[-1]
                if len(overlap_text) > chunk_overlap:
                    # Truncate overlap to desired size
                    overlap_text = overlap_text[-chunk_overlap:]
                current_chunk = [overlap_text] if overlap_text else []
                current_length = len(overlap_text)
            else:
                current_chunk = []
                current_length = 0
        
        current_chunk.append(sentence)
        current_length += sentence_length + 1  # +1 for space
    
    # Add final chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    # Fallback: if no sentences found or chunks too large, split by character
    if not chunks:
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - chunk_overlap)]
    
    return chunks

