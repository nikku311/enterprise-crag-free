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

class RiskAssessment(BaseModel):
    risk_level: Literal["low", "medium", "high", "critical"] = "low"
    risk_category: Literal["bias", "privacy", "hallucination", "toxicity", "none"] = "none"
    reasoning: str = ""
    requires_human_review: bool = False
    nist_mapping: str = ""
    eu_ai_act: str = ""

def get_risk_guard():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    
    structured_llm = llm.with_structured_output(RiskAssessment)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Assess AI output risk. Map to:
- NIST AI RMF: GOVERN/MAP/MEASURE/MANAGE
- EU AI Act: minimal/limited/high/unacceptable

HIGH/CRITICAL = human review needed
Bias in hiring/finance = HIGH
Medical/legal without disclaimer = HIGH
PII leak = CRITICAL"""),
        ("human", """Query: {query}
Context: {context}
Answer: {answer}

Assess risk.""")
    ])
    
    return prompt | structured_llm

def assess_risk(query: str, context: str, answer: str) -> RiskAssessment:
    return get_risk_guard().invoke({
        "query": query,
        "context": context,
        "answer": answer
    })

if __name__ == "__main__":
    result = assess_risk(
        "What is AI?",
        "AI is artificial intelligence",
        "AI stands for Artificial Intelligence"
    )
    print(f"Risk: {result.risk_level}, Review: {result.requires_human_review}")