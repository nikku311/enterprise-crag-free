from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

if __name__ == "__main__":
    emb = get_embeddings()
    vector = emb.embed_query("test sentence")
    print(f"Dimension: {len(vector)}")
    print(f"First 5: {vector[:5]}")