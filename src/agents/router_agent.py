import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

class RouteDecision(BaseModel):
    decision: Literal["direct", "retrieve"] = "direct"
    reasoning: str = ""

def get_router():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    
    structured_llm = llm.with_structured_output(RouteDecision)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a query router. Decide:
- "direct": greetings, general knowledge, simple questions
- "retrieve": specific facts, policies, technical details needing documents

Examples:
"Hello" → direct
"What is AI?" → direct
"What is our refund policy?" → retrieve"""),
        ("human", "{query}")
    ])
    
    return prompt | structured_llm

def route_query(query: str) -> RouteDecision:
    return get_router().invoke({"query": query})

if __name__ == "__main__":
    tests = ["Hello!", "What is machine learning?", "Company leave policy?"]
    for q in tests:
        r = route_query(q)
        print(f"{q} → {r.decision}")