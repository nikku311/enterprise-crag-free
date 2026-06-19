from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from src.tools.embeddings import get_embeddings

COLLECTION_NAME = "enterprise_docs"

def get_qdrant_client():
    """Local file mode - no Docker needed"""
    return QdrantClient(path="./qdrant_storage")

def create_collection():
    client = get_qdrant_client()
    collections = client.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)
    
    if not exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"Created: {COLLECTION_NAME}")
    return client

def get_vector_store():
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