# Enterprise Agentic RAG (CRAG) System

Self-correcting RAG with AI Governance. Free tier only.

## Architecture

## Tech Stack

| Layer | Tool | Cost |
|-------|------|------|
| LLM | Groq (Llama 3.3 70B) | Free |
| Embeddings | HuggingFace (local) | Free |
| Vector DB | Qdrant (local file) | Free |
| Web Search | DuckDuckGo | Free |
| Framework | LangGraph + FastAPI | Free |

## Governance

- NIST AI RMF aligned risk assessment
- EU AI Act risk classification
- DPDP India compliant audit logging
- Human-in-the-loop for high risk

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set GROQ_API_KEY in .env

# 3. Load sample data
python src/tools/data_loader.py

# 4. Start API
python src/api/main.py

# 5. Test
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d "{\"query\": \"What is AI safety?\"}"

src/
├── agents/         # Router, Retriever, Grader, Web Search, Generator
├── graph/          # LangGraph workflow
├── tools/          # Embeddings, Vector Store, Web Search, Data Loader
├── governance/     # Risk Guard, Audit Logger
└── api/            # FastAPI server


---

## Step 28: Git Commit

Terminal mein:

```bash
git add .
git commit -m "Complete CRAG system with AI governance"

