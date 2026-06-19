import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import streamlit as st
from src.graph.workflow import build_workflow

# Page config
st.set_page_config(
    page_title="Enterprise CRAG System",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 Enterprise Agentic RAG (CRAG)")
st.markdown("**AI Governance Enabled | Free Tier | Self-Correcting RAG**")

# Sidebar - Governance Info
with st.sidebar:
    st.header("🛡️ AI Governance")
    st.markdown("""
    **Frameworks Aligned:**
    - ✅ NIST AI RMF
    - ✅ EU AI Act
    - ✅ DPDP India 2023
    
    **Risk Levels:**
    🟢 Low | 🟡 Medium | 🔴 High | ⚫ Critical
    
    **Human Review Triggered for High/Critical**
    """)
    
    st.divider()
    st.markdown("**Tech Stack:**")
    st.markdown("""
    - 🤖 Groq (Llama 3.3 70B)
    - 🔍 HuggingFace Embeddings
    - 📊 Qdrant Vector DB
    - 🌐 DuckDuckGo Search
    - 🔄 LangGraph Workflow
    """)

# Main input
st.header("💬 Ask a Question")

query = st.text_input(
    "Enter your query:",
    placeholder="e.g., What is AI safety? What is our company policy?",
    key="query_input"
)

# Submit button
if st.button("🔍 Submit Query", type="primary"):
    if not query:
        st.warning("Please enter a query first!")
    else:
        with st.spinner("Processing through CRAG pipeline..."):
            try:
                # Run workflow
                workflow = build_workflow()
                result = workflow.invoke({"query": query})
                
                # Display results in columns
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("📋 Answer")
                    st.success(result["final_answer"])
                
                with col2:
                    st.subheader("📊 Pipeline Info")
                    
                    # Route
                    route_color = "🟢" if result["route"] == "direct" else "🔵"
                    st.markdown(f"{route_color} **Route:** {result['route'].upper()}")
                    
                    # Risk Level
                    risk = result["risk_level"]
                    if risk == "low":
                        risk_emoji = "🟢"
                    elif risk == "medium":
                        risk_emoji = "🟡"
                    elif risk == "high":
                        risk_emoji = "🔴"
                    else:
                        risk_emoji = "⚫"
                    
                    st.markdown(f"{risk_emoji} **Risk Level:** {risk.upper()}")
                    
                    # Human Review
                    if result["needs_review"]:
                        st.error("⚠️ Human Review Required!")
                    else:
                        st.success("✅ Auto-Approved")
                
                # Governance Badge
                st.divider()
                st.caption("🔒 Governed by NIST AI RMF | EU AI Act | DPDP India 2023")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Please make sure GROQ_API_KEY is set in .env file")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: gray;">
    <p>Built with ❤️ using LangGraph + Groq + Streamlit</p>
    <p>Free Tier | Open Source | AI Governance First</p>
</div>
""", unsafe_allow_html=True)