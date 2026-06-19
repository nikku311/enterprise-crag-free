import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.tools.vector_store import get_vector_store

def retrieve_documents(query: str, k: int = 4):
    store = get_vector_store()
    docs = store.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]

if __name__ == "__main__":
    print("Retriever ready - needs documents first")