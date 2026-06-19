import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.agents.router_agent import route_query
from src.tools.embeddings import get_embeddings

def test_router_direct():
    result = route_query("Hello!")
    assert result.decision == "direct"

def test_router_retrieve():
    result = route_query("What is company policy?")
    assert result.decision == "retrieve"

def test_embeddings():
    emb = get_embeddings()
    vector = emb.embed_query("test")
    assert len(vector) == 384

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])