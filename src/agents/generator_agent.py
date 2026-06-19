import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def get_generator():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant. Use provided context to answer.
If context is insufficient, say "I don't have enough information."
Always cite sources if context provided."""),
        ("human", """Context: {context}
Question: {query}
Answer:""")
    ])
    
    return prompt | llm

def generate_answer(query: str, context: str) -> str:
    chain = get_generator()
    result = chain.invoke({"query": query, "context": context})
    return result.content

if __name__ == "__main__":
    answer = generate_answer("What is RAG?", "RAG stands for Retrieval Augmented Generation")
    print(answer)