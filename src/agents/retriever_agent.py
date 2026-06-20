import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.tools.vector_store import get_vector_store

def retrieve_documents(query: str, k: int = 4):
    store = get_vector_store()
    docs = store.similarity_search(query, k=k)
    
    # Format with source info
    formatted = []
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        doc_type = doc.metadata.get("type", "text")
        
        header = f"[Source: {source} | Page: {page} | Type: {doc_type}]"
        formatted.append(f"{header}\n{doc.page_content}")
    
    return formatted