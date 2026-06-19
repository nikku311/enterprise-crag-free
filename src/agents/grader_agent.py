import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

class GradeResult(BaseModel):
    relevance: Literal["high", "medium", "low"] = "low"
    score: float = 0.0
    reasoning: str = ""

def get_grader():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    
    structured_llm = llm.with_structured_output(GradeResult)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Grade relevance of document to query.
Score 0-1, classify as high(>0.7), medium(0.4-0.7), low(<0.4)"""),
        ("human", """Query: {query}
Document: {document}

Grade relevance.""")
    ])
    
    return prompt | structured_llm

def grade_document(query: str, document: str) -> GradeResult:
    return get_grader().invoke({"query": query, "document": document})

if __name__ == "__main__":
    result = grade_document("AI safety", "AI safety prevents harmful outcomes")
    print(f"Score: {result.score}, Relevance: {result.relevance}")