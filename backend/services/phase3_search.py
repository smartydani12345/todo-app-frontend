import os
import requests
from typing import Dict, Any, List
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleSearchService:
    """
    Service to perform Google searches using various search APIs.
    Supports multiple search providers for flexibility.
    """

    def __init__(self):
        # Search API configuration
        # Using SerpAPI as primary (free tier available)
        self.serpapi_key = os.getenv("SERPAPI_KEY")
        # Alternative: Google Custom Search API
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.google_cse_id = os.getenv("GOOGLE_CSE_ID")
        
        # Default to using a free alternative if no API keys are set
        self.search_provider = os.getenv("SEARCH_PROVIDER", "duckduckgo")

    def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Perform a Google search and return results.

        Args:
            query: The search query
            num_results: Number of results to return (default: 5)

        Returns:
            Dictionary containing search results
        """
        try:
            if self.search_provider == "serpapi" and self.serpapi_key:
                return self._search_serpapi(query, num_results)
            elif self.search_provider == "google" and self.google_api_key and self.google_cse_id:
                return self._search_google_custom(query, num_results)
            else:
                # Fallback to DuckDuckGo HTML scraping (free, no API key needed)
                return self._search_duckduckgo(query, num_results)
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "results": [],
                "query": query
            }

    def _search_serpapi(self, query: str, num_results: int) -> Dict[str, Any]:
        """Search using SerpAPI."""
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.serpapi_key,
            "num": num_results
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        if "organic_results" in data:
            for result in data["organic_results"][:num_results]:
                results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })
        
        return {
            "success": True,
            "results": results,
            "query": query,
            "total_results": data.get("search_information", {}).get("total_results", 0)
        }

    def _search_google_custom(self, query: str, num_results: int) -> Dict[str, Any]:
        """Search using Google Custom Search API."""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.google_api_key,
            "cx": self.google_cse_id,
            "q": query,
            "num": min(num_results, 10)  # Google API max is 10
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        if "items" in data:
            for item in data["items"][:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
        
        return {
            "success": True,
            "results": results,
            "query": query,
            "total_results": data.get("searchInformation", {}).get("totalResults", 0)
        }

    def _search_duckduckgo(self, query: str, num_results: int) -> Dict[str, Any]:
        """
        Search using DuckDuckGo HTML page (free, no API key needed).
        This is a simple implementation that parses the HTML response.
        """
        try:
            # Use DuckDuckGo's HTML interface
            url = "https://html.duckduckgo.com/html/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            data = {"q": query}
            
            response = requests.post(url, data=data, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Simple parsing of DuckDuckGo HTML results
            results = []
            html_content = response.text
            
            # Extract result blocks (simplified parsing)
            import re
            
            # Find result titles and links
            title_pattern = r'class="result__title"[^>]*>([^<]+)'
            link_pattern = r'result__url[^>]*>([^<]+)'
            snippet_pattern = r'class="result__snippet"[^>]*>([^<]+)'
            
            titles = re.findall(title_pattern, html_content, re.IGNORECASE)
            links = re.findall(link_pattern, html_content, re.IGNORECASE)
            snippets = re.findall(snippet_pattern, html_content, re.IGNORECASE)
            
            for i in range(min(num_results, len(titles))):
                results.append({
                    "title": self._clean_html(titles[i]) if i < len(titles) else "",
                    "link": self._clean_html(links[i]) if i < len(links) else "",
                    "snippet": self._clean_html(snippets[i]) if i < len(snippets) else ""
                })
            
            return {
                "success": True,
                "results": results,
                "query": query,
                "total_results": len(results)
            }
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {str(e)}")
            # Return empty results on error
            return {
                "success": True,  # Still success, just no results
                "results": [],
                "query": query,
                "total_results": 0,
                "message": "Search temporarily unavailable"
            }

    def _clean_html(self, text: str) -> str:
        """Clean HTML entities from text."""
        import html
        return html.unescape(text).strip()

    def format_results_for_chat(self, search_results: Dict[str, Any]) -> str:
        """
        Format search results for chat response.

        Args:
            search_results: Dictionary containing search results

        Returns:
            Formatted string for chat response
        """
        if not search_results.get("success") or not search_results.get("results"):
            return "I couldn't find any relevant information for your query."
        
        formatted = "Here's what I found:\n\n"
        for i, result in enumerate(search_results["results"], 1):
            formatted += f"{i}. **{result['title']}**\n"
            formatted += f"   {result['snippet']}\n"
            formatted += f"   Source: {result['link']}\n\n"
        
        return formatted


# Global instance of the service
google_search_service = GoogleSearchService()


def get_search_service() -> GoogleSearchService:
    """
    Get the global instance of GoogleSearchService.

    Returns:
        GoogleSearchService instance
    """
    return google_search_service
