import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from langchain_core.documents import Document
from src.tools.vector_store import get_vector_store, create_collection

def load_sample_data():
    create_collection()
    store = get_vector_store()
    
    with open("data/sample_docs.txt", "r") as f:
        lines = f.readlines()
    
    docs = []
    for line in lines:
        if line.strip():
            docs.append(Document(page_content=line.strip()))
    
    store.add_documents(docs)
    print(f"Loaded {len(docs)} documents")

if __name__ == "__main__":
    load_sample_data()