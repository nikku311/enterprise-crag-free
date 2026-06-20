from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader,
    UnstructuredWordDocumentLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.tools.vector_store import get_vector_store
from src.tools.image_processor import process_image
from pathlib import Path

def load_document(file_path: str):
    """Universal document loader - PDF, TXT, DOCX, Image"""
    
    ext = Path(file_path).suffix.lower()
    
    # PDF
    if ext == '.pdf':
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        return _chunk_and_store(pages, source=Path(file_path).name)
    
    # Text
    elif ext in ['.txt', '.md']:
        loader = TextLoader(file_path)
        docs = loader.load()
        return _chunk_and_store(docs, source=Path(file_path).name)
    
    # Word
    elif ext in ['.docx', '.doc']:
        loader = UnstructuredWordDocumentLoader(file_path)
        docs = loader.load()
        return _chunk_and_store(docs, source=Path(file_path).name)
    
    # Image
    elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
        result = process_image(file_path)
        doc = Document(
            page_content=result["text"],
            metadata={"source": result["source"], "type": "image", "page": 1}
        )
        return _chunk_and_store([doc], source=result["source"])
    
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def _chunk_and_store(docs, source: str):
    """Common chunking and storage"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    
    store = get_vector_store()
    store.add_documents(chunks)
    
    return {
        "source": source,
        "chunks": len(chunks),
        "type": "success"
    }

if __name__ == "__main__":
    print("Document loader ready")