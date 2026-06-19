import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI
from pydantic import BaseModel
from src.graph.workflow import build_workflow

app = FastAPI(title="Enterprise CRAG API")

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query(request: QueryRequest):
    workflow = build_workflow()
    result = workflow.invoke({"query": request.query})
    
    return {
        "answer": result["final_answer"],
        "route": result["route"],
        "risk_level": result["risk_level"],
        "needs_human_review": result["needs_review"]
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)