"""
Web Search Service
Performs web searches using DuckDuckGo
"""

from duckduckgo_search import DDGS
import logging
from typing import Optional, List, Dict
from config import settings

logger = logging.getLogger(__name__)


class SearchService:
    """Handle web searches via DuckDuckGo"""
    
    def __init__(self):
        self.timeout = settings.DUCKDUCKGO_TIMEOUT
    
    def search(
        self,
        query: str,
        max_results: int = 3
    ) -> List[Dict]:
        """
        Perform web search using DuckDuckGo
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
        
        Returns:
            List of search results with title, body, and href
        """
        try:
            results = []
            ddgs = DDGS()
            
            # Perform search
            search_results = ddgs.text(query, max_results=max_results)
            
            for result in search_results:
                results.append({
                    "title": result.get("title", ""),
                    "summary": result.get("body", ""),
                    "url": result.get("href", ""),
                    "source": "Web Search"
                })
            
            if results:
                logger.info(f"Found {len(results)} web search results for: {query}")
            else:
                logger.info(f"No web search results found for: {query}")
            
            return results
        
        except Exception as e:
            logger.error(f"Error performing web search: {str(e)}")
            return []
    
    def summarize_results(self, results: List[Dict]) -> str:
        """
        Summarize search results into a single string
        
        Args:
            results: List of search results
        
        Returns:
            Formatted summary string
        """
        if not results:
            return ""
        
        summary = "\n".join([
            f"- {result['title']}: {result['summary'][:150]}..."
            for result in results[:3]
        ])
        
        return summary


# Global instance
search_service = SearchService()
