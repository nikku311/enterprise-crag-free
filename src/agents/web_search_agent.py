import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.tools.web_search import search_web

def web_search_fallback(query: str) -> str:
    return search_web(query)

if __name__ == "__main__":
    result = web_search_fallback("Latest AI safety news 2026")
    print(result[:500])