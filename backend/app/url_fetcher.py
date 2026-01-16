"""
URL content fetching and extraction
"""
import httpx
from bs4 import BeautifulSoup
import logging
from typing import Optional

logger = logging.getLogger(__name__)


async def fetch_url_content(url: str) -> Optional[str]:
    """
    Fetch and extract text content from a URL
    
    Args:
        url: URL to fetch
        
    Returns:
        Extracted text content or None if failed
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text if text else None
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching URL {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return None

