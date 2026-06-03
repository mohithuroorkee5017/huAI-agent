"""
Wikipedia Search Service
Fetches information from Wikipedia
"""

import wikipedia
import logging
from typing import Optional, Dict
from config import settings

logger = logging.getLogger(__name__)


class WikipediaService:
    """Handle Wikipedia searches and summaries"""
    
    def __init__(self):
        self.timeout = settings.WIKIPEDIA_TIMEOUT
        # Set language for Wikipedia
        self.languages = {
            "hi": "hi",      # Hindi
            "en": "en",      # English
            "en-IN": "en"    # English (India)
        }
    
    def search(
        self,
        query: str,
        language: str = "en"
    ) -> Optional[Dict]:
        """
        Search Wikipedia and return summary
        
        Args:
            query: Search query
            language: Language code (hi, en)
        
        Returns:
            Dict with title, summary, and url or None if not found
        """
        try:
            # Set Wikipedia language
            wiki_lang = self.languages.get(language, "en")
            wikipedia.set_lang(wiki_lang)
            
            # Search for query
            results = wikipedia.search(query, results=3)
            
            if not results:
                logger.info(f"No Wikipedia results found for: {query}")
                return None
            
            try:
                # Get summary of first result
                summary = wikipedia.summary(results[0], sentences=3)
                page = wikipedia.page(results[0], auto_suggest=False)
                
                return {
                    "title": page.title,
                    "summary": summary,
                    "url": page.url,
                    "source": "Wikipedia"
                }
            except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError, wikipedia.exceptions.InvalidPageError) as e:
                logger.warning(f"Wikipedia page error for '{results[0]}': {str(e)}")
                return None
        
        except wikipedia.exceptions.DisambiguationError as e:
            logger.warning(f"Disambiguation error for {query}: {str(e)}")
            return None
        
        except wikipedia.exceptions.PageError:
            logger.info(f"Page not found for: {query}")
            return None
        
        except Exception as e:
            logger.error(f"Error searching Wikipedia: {type(e).__name__} - {str(e)}")
            return None


# Global instance
wiki_service = WikipediaService()
