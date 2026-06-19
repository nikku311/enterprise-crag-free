import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from typing import TypedDict, List
from langgraph.graph import StateGraph, END

from src.agents.router_agent import route_query
from src.agents.retriever_agent import retrieve_documents
from src.agents.grader_agent import grade_document
from src.agents.web_search_agent import web_search_fallback
from src.agents.generator_agent import generate_answer
from src.governance.risk_guard import assess_risk
from src.governance.audit_logger import AuditLogger

class CRAGState(TypedDict):
    query: str
    route: str
    documents: List[str]
    graded_docs: List[str]
    web_results: str
    final_answer: str
    risk_level: str
    needs_review: bool

logger = AuditLogger()

def router_node(state: CRAGState):
    result = route_query(state["query"])
    return {"route": result.decision}

def retrieve_node(state: CRAGState):
    if state["route"] == "direct":
        return {"documents": []}
    docs = retrieve_documents(state["query"])
    return {"documents": docs}

def grade_node(state: CRAGState):
    if not state["documents"]:
        return {"graded_docs": []}
    
    good_docs = []
    for doc in state["documents"]:
        grade = grade_document(state["query"], doc)
        if grade.relevance in ["high", "medium"]:
            good_docs.append(doc)
    
    return {"graded_docs": good_docs}

def fallback_node(state: CRAGState):
    if not state["graded_docs"]:
        result = web_search_fallback(state["query"])
        return {"web_results": result}
    return {"web_results": ""}

def generate_node(state: CRAGState):
    context = "\n".join(state["graded_docs"]) or state["web_results"] or "No relevant context found."
    answer = generate_answer(state["query"], context)
    return {"final_answer": answer}

def risk_node(state: CRAGState):
    context = "\n".join(state["graded_docs"]) or state["web_results"] or ""
    risk = assess_risk(state["query"], context, state["final_answer"])
    
    logger.log(
        state["query"],
        state["route"],
        risk.risk_level,
        state["final_answer"]
    )
    
    return {
        "risk_level": risk.risk_level,
        "needs_review": risk.requires_human_review
    }

def build_workflow():
    workflow = StateGraph(CRAGState)
    
    workflow.add_node("router", router_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("grade", grade_node)
    workflow.add_node("fallback", fallback_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("risk", risk_node)
    
    workflow.set_entry_point("router")
    workflow.add_edge("router", "retrieve")
    workflow.add_edge("retrieve", "grade")
    workflow.add_edge("grade", "fallback")
    workflow.add_edge("fallback", "generate")
    workflow.add_edge("generate", "risk")
    workflow.add_edge("risk", END)
    
    return workflow.compile()

if __name__ == "__main__":
    app = build_workflow()
    result = app.invoke({"query": "What is machine learning?"})
    print(f"Answer: {result['final_answer']}")
    print(f"Risk: {result['risk_level']}")