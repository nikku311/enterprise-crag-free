import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))

from src.graph.workflow import build_workflow
from src.tools.document_loader import load_document

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Enterprise CRAG | AI Governance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# THEME / CSS
# ============================================================
st.markdown("""
<style>
    #MainMenu, footer {visibility: hidden;}
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1b1840 45%, #16213e 100%);
        color: #e6e6f0;
    }
    /* Streamlit's own top toolbar (Deploy / menu) — match it to the dark theme
       and stop it from sitting transparently over our content */
    [data-testid="stHeader"] {
        background: #0f0c29 !important;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        height: 3.2rem;
    }
    [data-testid="stToolbar"] { right: 1rem; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #15152b 0%, #161e34 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1rem; }
    /* Enough top padding so content clears the fixed toolbar above (prevents clipping) */
    .block-container { padding-top: 2.6rem; padding-bottom: 1rem; max-width: 1100px; }

    /* ---------- Header ---------- */
    .app-header { display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;
                  padding: 6px 4px 14px 4px; border-bottom: 1px solid rgba(255,255,255,0.08); }
    .app-title { font-size: 2em; font-weight: 800; margin:0; line-height:1.35; padding-top:4px;
                 background: linear-gradient(90deg, #00d4ff, #9b5cff);
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .app-subtitle { color: #8b8ba7; letter-spacing: 1.5px; font-size: 0.78em; margin-top: 2px; }
    .status-pill { display:inline-flex; align-items:center; gap:7px; background: rgba(0,255,136,0.1);
                   border: 1px solid rgba(0,255,136,0.3); padding: 6px 16px; border-radius: 20px;
                   font-size: 0.82em; color:#00ff88; font-weight:600; white-space:nowrap; }
    .status-dot { width:8px; height:8px; border-radius:50%; background:#00ff88;
                  box-shadow:0 0 8px #00ff88; animation: pulse 2s infinite; }
    @keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.35;} }

    /* ---------- Sidebar ---------- */
    .sb-title { color:#00d4ff; font-size:1.25em; font-weight:700; margin:0; }
    .sb-sub { color:#666; font-size:0.78em; margin-top:2px; }
    .sb-section { color:#7a7a99; font-size:0.72em; font-weight:700; letter-spacing:1.5px;
                  text-transform:uppercase; margin: 16px 0 8px 2px; }

    .fw-badge { display:flex; align-items:center; gap:8px; padding:9px 10px; border-radius:8px;
                margin-bottom:7px; font-size:0.86em; font-weight:500; line-height:1.3; }
    .fw-nist { background: rgba(0,255,136,0.08); border-left:3px solid #00ff88; color:#cdfff0; }
    .fw-eu   { background: rgba(0,212,255,0.08); border-left:3px solid #00d4ff; color:#cdf2ff; }
    .fw-dpdp { background: rgba(155,92,255,0.10); border-left:3px solid #9b5cff; color:#e6d9ff; }

    .risk-grid { display:grid; grid-template-columns:1fr 1fr; gap:7px; }
    .risk-chip { padding:8px 4px; border-radius:8px; text-align:center; font-weight:700; font-size:0.78em; }

    .doc-card { background: rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
                border-radius:10px; padding:9px 11px; }
    .doc-card .name { color:#e6e6f0; font-weight:600; font-size:0.85em; word-break:break-word; }
    .doc-card .meta { color:#7a7a99; font-size:0.72em; margin-top:1px; }

    [data-testid="stMetric"] { background: rgba(0,212,255,0.05); border:1px solid rgba(0,212,255,0.15);
                                border-radius:12px; padding:8px 4px; }
    [data-testid="stMetricValue"] { color:#fff; }
    [data-testid="stMetricLabel"] { color:#8b8ba7; }

    /* ---------- Global text readability ----------
       Streamlit's default markdown text color can come out near-invisible
       against our custom dark background, so it's forced explicitly here. */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span,
    .stMarkdown strong, .stMarkdown em, .stMarkdown ol, .stMarkdown ul,
    [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li, [data-testid="stMarkdownContainer"] span {
        color: #e9e9f3 !important;
    }
    .stMarkdown code, [data-testid="stMarkdownContainer"] code {
        color: #00d4ff !important; background: rgba(0,212,255,0.08) !important;
    }
    .stMarkdown a, [data-testid="stMarkdownContainer"] a { color: #00d4ff !important; }
    label, .stCaption, [data-testid="stWidgetLabel"] p { color: #c4c4d6 !important; }

    /* ---------- Chat ---------- */
    [data-testid="stChatMessage"] { background: rgba(255,255,255,0.045);
        border:1px solid rgba(255,255,255,0.1); border-radius:14px; }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
        font-size: 1.0em; line-height: 1.55;
    }


    .gov-strip { display:flex; gap:8px; flex-wrap:wrap; margin-top:10px; padding-top:10px;
                 border-top:1px solid rgba(255,255,255,0.08); }
    .gov-tag { font-size:0.7em; font-weight:700; padding:4px 11px; border-radius:20px; letter-spacing:0.4px; }

    .welcome-card { background: rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.09);
                    border-radius:16px; padding: 26px 24px; text-align:center; }
    .welcome-card h3 { color:#00d4ff; margin-bottom:6px; }
    .welcome-card p { color:#9494ad; font-size:0.92em; }

    /* ---------- Buttons / inputs ---------- */
    .stButton > button { background: linear-gradient(90deg, #667eea 0%, #9b5cff 100%);
        color:white; border:none; border-radius:20px; font-weight:600;
        box-shadow:0 4px 14px rgba(102,126,234,0.3); }
    .stButton > button:hover { transform: translateY(-1px); box-shadow:0 8px 18px rgba(102,126,234,0.5); }
    [data-testid="stChatInput"] textarea {
        border-radius:14px !important; color:#1a1a2e !important;
    }
    [data-testid="stChatInput"] textarea::placeholder { color:#6b6b80 !important; }

    ::-webkit-scrollbar { width:7px; }
    ::-webkit-scrollbar-track { background:#0f0c29; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(180deg,#00d4ff,#9b5cff); border-radius:4px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
st.session_state.setdefault("uploaded_docs", [])       # [{name, chunks, type, file_id}]
st.session_state.setdefault("processed_file_ids", set())
st.session_state.setdefault("chat_history", [])         # [{role, content, meta}]
st.session_state.setdefault("query_count", 0)

RISK_COLORS = {"low": "#00ff88", "medium": "#ffaa00", "high": "#ff4444", "critical": "#ff0000"}
TYPE_ICON = {"pdf": "📄", "docx": "📝", "txt": "📃", "png": "🖼️", "jpg": "🖼️", "jpeg": "🖼️"}


@st.cache_resource
def get_workflow():
    """Build the LangGraph workflow once and reuse across queries."""
    return build_workflow()


def file_icon(filename: str) -> str:
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    return TYPE_ICON.get(ext, "📁")


def run_query(query_text: str):
    """Send a query through the CRAG pipeline and store the result in chat history."""
    st.session_state.chat_history.append({"role": "user", "content": query_text})
    st.session_state.query_count += 1

    try:
        workflow = get_workflow()
        result = workflow.invoke({"query": query_text})
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": result.get("final_answer", "_No answer was generated._"),
            "meta": {
                "route": result.get("route", "unknown"),
                "risk_level": result.get("risk_level", "low"),
                "needs_review": result.get("needs_review", False),
                "error": False,
            }
        })
    except Exception as e:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"**Something went wrong while processing your query.**\n\n`{str(e)}`\n\n"
                        f"Please make sure `GROQ_API_KEY` is configured correctly.",
            "meta": {"error": True}
        })


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding-bottom:14px; border-bottom:1px solid rgba(255,255,255,0.08);">
        <div class="sb-title">🛡️ AI Governance</div>
        <div class="sb-sub">Enterprise-Grade Compliance</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Frameworks Aligned</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="fw-badge fw-nist">✓&nbsp; NIST AI RMF</div>
        <div class="fw-badge fw-eu">✓&nbsp; EU AI Act</div>
        <div class="fw-badge fw-dpdp">✓&nbsp; DPDP India 2023</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Risk Classification</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="risk-grid">
            <div class="risk-chip" style="background:rgba(0,255,136,0.1); color:#00ff88;">LOW</div>
            <div class="risk-chip" style="background:rgba(255,170,0,0.1); color:#ffaa00;">MEDIUM</div>
            <div class="risk-chip" style="background:rgba(255,68,68,0.1); color:#ff4444;">HIGH</div>
            <div class="risk-chip" style="background:rgba(255,0,0,0.1); color:#ff0000;">CRITICAL</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Document Upload</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Drop files here",
        type=["pdf", "txt", "docx", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="PDF, TXT, DOCX, PNG, JPG — up to 200MB per file"
    )

    if uploaded_files:
        new_files = []
        for f in uploaded_files:
            fid = f"{f.name}_{len(f.getvalue())}"
            if fid not in st.session_state.processed_file_ids:
                new_files.append((f, fid))

        if new_files:
            progress = st.progress(0, text="Starting...")
            for i, (f, fid) in enumerate(new_files):
                temp_path = f"temp_{f.name}"
                try:
                    with open(temp_path, "wb") as out:
                        out.write(f.getvalue())
                    progress.progress((i) / len(new_files), text=f"Processing {f.name}...")
                    result = load_document(temp_path)
                    st.session_state.uploaded_docs.append({
                        "name": f.name,
                        "chunks": result["chunks"],
                        "type": result["type"],
                        "file_id": fid,
                    })
                    st.session_state.processed_file_ids.add(fid)
                except Exception as e:
                    st.error(f"❌ {f.name}: {e}")
                progress.progress((i + 1) / len(new_files))
            progress.empty()
            st.rerun()

    if st.session_state.uploaded_docs:
        st.markdown('<div class="sb-section">Indexed Documents</div>', unsafe_allow_html=True)
        for idx, doc in enumerate(st.session_state.uploaded_docs):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"""
                <div class="doc-card">
                    <div class="name">{file_icon(doc['name'])} {doc['name']}</div>
                    <div class="meta">{doc['chunks']} chunks • {doc['type']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("✕", key=f"del_{doc['file_id']}", help="Remove document"):
                    st.session_state.processed_file_ids.discard(doc["file_id"])
                    st.session_state.uploaded_docs.pop(idx)
                    st.rerun()

        st.markdown('<div class="sb-section">System Stats</div>', unsafe_allow_html=True)
        sc1, sc2 = st.columns(2)
        sc1.metric("Documents", len(st.session_state.uploaded_docs))
        sc2.metric("Queries", st.session_state.query_count)

    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Everything", use_container_width=True):
        st.session_state.uploaded_docs = []
        st.session_state.processed_file_ids = set()
        st.session_state.chat_history = []
        st.session_state.query_count = 0
        st.rerun()

# ============================================================
# MAIN — HEADER
# ============================================================
st.markdown("""
<div class="app-header">
    <div>
        <div class="app-title">🛡️ Enterprise CRAG</div>
        <div class="app-subtitle">CORRECTIVE RAG WITH AI GOVERNANCE</div>
    </div>
    <div class="status-pill"><span class="status-dot"></span> System Online</div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.uploaded_docs:
    st.info("📁 Upload documents from the sidebar to ask questions grounded in your files — or just ask a general question below.", icon="💡")

# ============================================================
# MAIN — CHAT
# ============================================================
chat_box = st.container(height=460, border=False)

with chat_box:
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="welcome-card">
            <h3>💬 Ask anything about your documents</h3>
            <p>Try: "What is the maternity leave policy?" or "Summarize this document"</p>
        </div>
        """, unsafe_allow_html=True)

        examples = ["Summarize the document", "What is the maternity leave policy?", "List the key risks mentioned"]
        cols = st.columns(len(examples))
        for col, ex in zip(cols, examples):
            with col:
                if st.button(ex, use_container_width=True, key=f"ex_{ex}"):
                    run_query(ex)
                    st.rerun()
    else:
        for msg in st.session_state.chat_history:
            avatar = "🧑‍💻" if msg["role"] == "user" else "🛡️"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

                meta = msg.get("meta")
                if meta and not meta.get("error"):
                    route = meta["route"]
                    risk = meta["risk_level"]
                    risk_color = RISK_COLORS.get(risk, "#888")
                    review = meta["needs_review"]
                    status_color = "#ff4444" if review else "#00ff88"
                    status_text = "⚠️ REVIEW REQUIRED" if review else "✅ AUTO-APPROVED"

                    st.markdown(f"""
                    <div class="gov-strip">
                        <span class="gov-tag" style="background:rgba(0,212,255,0.12); color:#00d4ff;">
                            ROUTE: {route.upper()}</span>
                        <span class="gov-tag" style="background:rgba(255,255,255,0.06); color:{risk_color};">
                            RISK: {risk.upper()}</span>
                        <span class="gov-tag" style="background:rgba(255,255,255,0.06); color:{status_color};">
                            {status_text}</span>
                    </div>
                    """, unsafe_allow_html=True)

# ============================================================
# MAIN — INPUT
# ============================================================
query = st.chat_input("Ask a question about your documents...")
if query:
    with st.spinner("Processing through CRAG pipeline..."):
        run_query(query)
    st.rerun()

st.markdown("""
<div style="text-align:center; padding:14px 0 4px; color:#555; font-size:0.78em;">
    Built with ❤ using <span style="color:#00d4ff;">LangGraph</span> +
    <span style="color:#9b5cff;">Groq</span> + <span style="color:#ff4444;">Streamlit</span>
    &nbsp;•&nbsp; Governed by NIST AI RMF, EU AI Act, DPDP India 2023
</div>
""", unsafe_allow_html=True)