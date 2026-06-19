from langchain_community.tools import DuckDuckGoSearchRun

def search_web(query: str) -> str:
    """Free web search - no API key needed"""
    search = DuckDuckGoSearchRun()
    try:
        return search.run(query)
    except Exception as e:
        return f"Search error: {str(e)}"

if __name__ == "__main__":
    result = search_web("What is agentic RAG?")
    print(result[:500])