from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from src.tools.embeddings import get_embeddings

COLLECTION_NAME = "enterprise_docs"
QDRANT_PATH = "./qdrant_storage"

# SINGLE shared client instance
_client = None

def get_qdrant_client():
    """Singleton client - ensures same instance is always used"""
    global _client
    if _client is None:
        _client = QdrantClient(path=QDRANT_PATH)
    return _client

def create_collection():
    client = get_qdrant_client()
    try:
        collections = client.get_collections().collections
        exists = any(c.name == COLLECTION_NAME for c in collections)
    except Exception:
        exists = False
    
    if not exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"Created: {COLLECTION_NAME}")
    return client

def get_vector_store():
    create_collection()
    
    embeddings = get_embeddings()
    client = get_qdrant_client()
    
    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )

if __name__ == "__main__":
    create_collection()
    store = get_vector_store()
    print("Ready!")