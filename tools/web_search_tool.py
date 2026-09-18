import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tavily import TavilyClient
from config.settings import TAVILY_API_KEY

_client = None


def _get_client():
    global _client
    if _client is None:
        if not TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY not set in .env")
        _client = TavilyClient(api_key=TAVILY_API_KEY)
    return _client


def search_facts(query: str) -> str:
    try:
        client = _get_client()
        result = client.search(
            query=query,
            search_depth="basic",
            include_answer=True,
            max_results=3,
        )
        return result.get("answer", "") or ""
    except Exception as e:
        print(f"Tavily search failed: {e}")
        return ""


if __name__ == "__main__":
    print(search_facts("travel time and distance from Nagpur to Delhi by train"))
