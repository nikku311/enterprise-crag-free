import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, field_validator
from typing import Literal

load_dotenv()

class RiskAssessment(BaseModel):
    risk_level: Literal["low", "medium", "high", "critical"] = "low"
    risk_category: Literal["bias", "privacy", "hallucination", "toxicity", "none"] = "none"
    content_type: Literal["text", "image", "mixed"] = "text"
    pii_detected: bool = False
    doc_classification: Literal["public", "internal", "confidential", "restricted"] = "internal"
    reasoning: str = ""
    requires_human_review: bool = False
    nist_mapping: str = ""
    eu_ai_act: str = ""
    
    @field_validator('requires_human_review', mode='before')
    @classmethod
    def parse_bool(cls, v):
        if isinstance(v, str):
            return v.lower() in ('true', 'yes', '1')
        return v
    
    @field_validator('pii_detected', mode='before')
    @classmethod
    def parse_pii(cls, v):
        if isinstance(v, str):
            return v.lower() in ('true', 'yes', '1', 'detected')
        return v

def get_risk_guard():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    
    structured_llm = llm.with_structured_output(RiskAssessment)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an AI Risk Assessment system for enterprise document analysis.

Assess output risk based on:
1. Content sensitivity (PII, financial, medical, legal)
2. Document classification (Public/Internal/Confidential/Restricted)
3. Content type (Text/Image/Mixed)
4. Source trustworthiness

Additional checks for uploaded documents:
- Image contains sensitive PII? (faces, signatures, IDs, Aadhaar, PAN)
- Document classification: Internal/Confidential/Public
- Source verification: Is this from trusted upload?
- Bias in hiring/finance = HIGH
- Medical/legal advice without disclaimer = HIGH
- PII leak = CRITICAL
- Image with faces/government IDs = HIGH

Map to frameworks:
- NIST AI RMF: GOVERN/MAP/MEASURE/MANAGE
- EU AI Act: minimal/limited/high/unacceptable
- DPDP India: Personal data protection

HIGH/CRITICAL = human review needed"""),
        ("human", """Query: {query}
Context: {context}
Answer: {answer}

Assess risk. Return structured output with all fields.""")
    ])
    
    return prompt | structured_llm

def assess_risk(query: str, context: str, answer: str) -> RiskAssessment:
    return get_risk_guard().invoke({
        "query": query,
        "context": context,
        "answer": answer
    })

if __name__ == "__main__":
    # Test 1: Safe text
    result1 = assess_risk(
        "What is AI?",
        "AI is artificial intelligence",
        "AI stands for Artificial Intelligence"
    )
    print(f"Test 1 - Risk: {result1.risk_level}, PII: {result1.pii_detected}, Doc: {result1.doc_classification}")
    
    # Test 2: Image with potential PII
    result2 = assess_risk(
        "What is in this document?",
        "[Image: Aadhaar card scan, Name: Rahul Sharma, Aadhaar: 1234-5678-9012]",
        "The document shows an Aadhaar card belonging to Rahul Sharma"
    )
    print(f"Test 2 - Risk: {result2.risk_level}, PII: {result2.pii_detected}, Doc: {result2.doc_classification}")