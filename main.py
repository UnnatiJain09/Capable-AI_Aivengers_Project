"""
AcademicAI — Subject Guide & Question Bank Assistant
=====================================================
Main Streamlit Application
"""

from __future__ import annotations

import os
import sys
import time
import tempfile
from pathlib import Path
from typing import List, Dict, Optional

import streamlit as st

# ── Path fix ──────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent))

# ── Page config (must be first Streamlit call) ────────────────────
st.set_page_config(
    page_title="AcademicAI — Subject Guide & Question Bank",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Root Variables ── */
:root {
    --bg: #080d1a;
    --bg2: #0f1629;
    --card: #131e35;
    --card2: #1a2540;
    --border: rgba(99,102,241,0.2);
    --accent: #6366f1;
    --accent2: #818cf8;
    --purple: #8b5cf6;
    --teal: #14b8a6;
    --green: #10b981;
    --amber: #f59e0b;
    --red: #ef4444;
    --text: #e2e8f0;
    --text2: #94a3b8;
    --text3: #64748b;
    --glow: rgba(99,102,241,0.25);
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background: var(--bg) !important; }

/* ── Hide default Streamlit elements ── */
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 3px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1rem !important; }

/* ── Top Header Bar ── */
.top-header {
    background: linear-gradient(135deg, var(--card) 0%, var(--card2) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 0 40px var(--glow);
    position: relative;
    overflow: hidden;
}
.top-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--purple), var(--teal));
}
.top-header h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #fff 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 !important; padding: 0 !important;
}
.top-header .tagline {
    color: var(--text2);
    font-size: 0.85rem;
    margin-top: 2px;
}
.header-logo { font-size: 2.4rem; }

/* ── Stat Cards ── */
.stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.stat-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 24px var(--glow);
    transform: translateY(-2px);
}
.stat-card .stat-icon { font-size: 1.8rem; margin-bottom: 0.4rem; }
.stat-card .stat-value {
    font-size: 2rem;
    font-weight: 700;
    font-family: 'Space Grotesk', sans-serif;
    color: var(--accent2);
}
.stat-card .stat-label {
    font-size: 0.78rem;
    color: var(--text2);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.2rem;
}

/* ── Section Cards ── */
.section-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Chat Messages ── */
.chat-wrapper { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1rem; }

.msg-user {
    display: flex;
    justify-content: flex-end;
    animation: slideInRight 0.3s ease;
}
.msg-ai {
    display: flex;
    justify-content: flex-start;
    animation: slideInLeft 0.3s ease;
}

.bubble-user {
    background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%);
    color: white;
    padding: 0.9rem 1.2rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 70%;
    font-size: 0.93rem;
    line-height: 1.6;
    box-shadow: 0 4px 16px rgba(99,102,241,0.4);
}

.bubble-ai {
    background: var(--card2);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 1rem 1.2rem;
    border-radius: 18px 18px 18px 4px;
    max-width: 80%;
    font-size: 0.92rem;
    line-height: 1.7;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.bubble-ai h2, .bubble-ai h3 { color: var(--accent2) !important; font-size: 0.95rem !important; }
.bubble-ai strong { color: var(--text) !important; }
.bubble-ai code {
    background: rgba(99,102,241,0.15);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.88em;
    color: var(--accent2);
}

.avatar-ai {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--accent), var(--purple));
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    margin-right: 0.6rem;
    align-self: flex-end;
    box-shadow: 0 0 12px var(--glow);
}

/* ── Query Type Badge ── */
.qtype-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}
.badge-topic { background: rgba(99,102,241,0.2); color: var(--accent2); border: 1px solid rgba(99,102,241,0.3); }
.badge-question { background: rgba(245,158,11,0.15); color: var(--amber); border: 1px solid rgba(245,158,11,0.3); }
.badge-quiz { background: rgba(16,185,129,0.15); color: var(--green); border: 1px solid rgba(16,185,129,0.3); }

/* ── Source Attribution ── */
.source-chip {
    display: inline-block;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.25);
    color: var(--text2);
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    margin: 2px;
    transition: all 0.2s;
}
.source-chip:hover {
    background: rgba(99,102,241,0.2);
    color: var(--accent2);
}

/* ── Upload Zone ── */
.upload-hint {
    background: var(--card);
    border: 2px dashed var(--border);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    color: var(--text2);
    margin-bottom: 1rem;
    transition: border-color 0.3s;
}
.upload-hint:hover { border-color: var(--accent); }

/* ── Doc Card ── */
.doc-card {
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    transition: all 0.2s;
}
.doc-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 12px var(--glow);
}
.doc-type-badge {
    padding: 3px 9px;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.badge-qp  { background: rgba(245,158,11,0.15); color: var(--amber); }
.badge-lab { background: rgba(20,184,166,0.15); color: var(--teal); }
.badge-lec { background: rgba(99,102,241,0.15); color: var(--accent2); }
.badge-txt { background: rgba(16,185,129,0.15); color: var(--green); }

/* ── Nav Buttons in Sidebar ── */
.nav-btn {
    width: 100%;
    padding: 0.7rem 1rem;
    border-radius: 10px;
    border: 1px solid transparent;
    background: transparent;
    color: var(--text2);
    text-align: left;
    cursor: pointer;
    font-size: 0.92rem;
    font-family: 'Inter', sans-serif;
    transition: all 0.2s;
    margin-bottom: 0.3rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.nav-btn:hover, .nav-btn.active {
    background: rgba(99,102,241,0.15);
    border-color: rgba(99,102,241,0.3);
    color: var(--accent2);
}

/* ── Feature Cards (Home) ── */
.feature-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem;
    text-align: center;
    transition: all 0.3s;
    height: 100%;
}
.feature-card:hover {
    border-color: var(--accent);
    box-shadow: 0 8px 32px var(--glow);
    transform: translateY(-4px);
}
.feature-card .f-icon { font-size: 2.2rem; margin-bottom: 0.8rem; }
.feature-card h3 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: var(--text) !important;
    margin-bottom: 0.5rem !important;
}
.feature-card p { color: var(--text2); font-size: 0.83rem; line-height: 1.6; }

/* ── Streamlit overrides ── */
div[data-testid="stChatInput"] > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}
div[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--purple)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.5) !important;
}
.stSelectbox > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}
.stTextInput > div > div > input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
}
.stTextArea > div > div > textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
}

/* ── Progress bars ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--purple)) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--card) !important;
    border-radius: 8px !important;
    color: var(--text2) !important;
    font-size: 0.82rem !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Animations ── */
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(20px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.animate-fade { animation: fadeIn 0.4s ease; }
.animate-pulse { animation: pulse 1.5s infinite; }

/* ── Typing indicator ── */
.typing-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: var(--accent2);
    border-radius: 50%;
    margin: 0 2px;
    animation: pulse 1s infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

/* ── Welcome Banner ── */
.welcome-banner {
    background: linear-gradient(135deg, #0f1629 0%, #1a1040 50%, #0f1629 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 2rem;
}
.welcome-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--purple), var(--teal), var(--accent));
    background-size: 200% auto;
    animation: shine 3s linear infinite;
}
@keyframes shine {
    from { background-position: 0% center; }
    to { background-position: 200% center; }
}
.welcome-banner h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #fff 0%, var(--accent2) 60%, var(--purple) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.8rem !important;
}
.welcome-banner p { color: var(--text2); font-size: 1rem; max-width: 600px; margin: 0 auto; }

/* ── API Key Warning ── */
.api-warning {
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.3);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: var(--amber);
    font-size: 0.88rem;
    margin-bottom: 1rem;
}
.api-warning a { color: var(--accent2); }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
#  Session State Initialisation
# ─────────────────────────────────────────────────────────────────

def init_session():
    defaults = {
        "page": "home",
        "chat_history": [],           # [{role, content, docs, qtype}]
        "uploaded_docs": [],          # [{name, subject, content_type, chunks}]
        "active_subject": "All Subjects",
        "api_key_valid": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


def set_page(page_name: str):
    st.session_state.page = page_name


def set_question_pending(ex_text: str):
    st.session_state["_question_pending"] = ex_text



# ─────────────────────────────────────────────────────────────────
#  Imports (deferred to allow CSS to load first)
# ─────────────────────────────────────────────────────────────────

try:
    from app.config import GOOGLE_API_KEY, UPLOADS_PATH
    from app.document_processing.processors import (
        process_uploaded_file, get_content_type_emoji
    )
    from app.vector_store.chroma_store import (
        add_documents, get_collection_stats,
        collection_exists_and_has_docs, delete_document
    )
    from app.agent.agent_core import chat, get_topic_summary
    MODULES_OK = True
except Exception as e:
    MODULES_OK = False
    MODULE_ERROR = str(e)


# ─────────────────────────────────────────────────────────────────
#  Helper: Content-type badge HTML
# ─────────────────────────────────────────────────────────────────

def ct_badge(content_type: str) -> str:
    labels = {
        "question_paper": ("📝 Q-Paper", "badge-qp"),
        "lab_manual":     ("🔬 Lab Manual", "badge-lab"),
        "lecture_notes":  ("📋 Lecture Notes", "badge-lec"),
        "textbook":       ("📚 Textbook", "badge-txt"),
    }
    label, cls = labels.get(content_type, (f"📄 {content_type}", "badge-txt"))
    return f'<span class="doc-type-badge {cls}">{label}</span>'


def qtype_badge_html(qtype: str) -> str:
    if qtype == "question_solver":
        return '<span class="qtype-badge badge-question">🎯 Question Solver</span>'
    elif qtype == "quiz":
        return '<span class="qtype-badge badge-quiz">📝 Quiz Mode</span>'
    else:
        return '<span class="qtype-badge badge-topic">📖 Topic Explanation</span>'


# ─────────────────────────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="text-align:center; padding: 1rem 0 1.5rem;">
            <div style="font-size:2.8rem;">📚</div>
            <div style="font-family:'Space Grotesk',sans-serif; font-size:1.2rem; font-weight:700; 
                        background:linear-gradient(135deg,#fff,#818cf8); -webkit-background-clip:text;
                        -webkit-text-fill-color:transparent; background-clip:text;">
                AcademicAI
            </div>
            <div style="font-size:0.72rem; color:#64748b; margin-top:2px;">Subject Guide & Question Bank</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Navigation
        nav_items = [
            ("home",      "🏠", "Home"),
            ("upload",    "📁", "Upload Documents"),
            ("chat",      "🧠", "Chat Assistant"),
            ("questions", "📝", "Question Solver"),
            ("dashboard", "📊", "Dashboard"),
        ]
        for page_id, icon, label in nav_items:
            active = "active" if st.session_state.page == page_id else ""
            st.button(
                f"{icon}  {label}",
                key=f"nav_{page_id}",
                use_container_width=True,
                on_click=set_page,
                args=(page_id,),
            )

        st.divider()

        # Subject Filter
        stats = {}
        if MODULES_OK:
            try:
                stats = get_collection_stats()
            except Exception:
                pass

        subjects = ["All Subjects"] + stats.get("subjects", [])
        st.session_state.active_subject = st.selectbox(
            "🎯 Active Subject",
            subjects,
            index=0,
            key="subject_selector",
        )

        st.divider()

        # Quick Stats
        if stats.get("total_chunks", 0) > 0:
            st.markdown(f"""
            <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase; 
                        letter-spacing:0.06em; margin-bottom:0.6rem;">Library Stats</div>
            <div style="display:flex; flex-direction:column; gap:0.4rem;">
                <div style="background:#131e35; border-radius:8px; padding:0.5rem 0.8rem;
                            font-size:0.82rem; color:#94a3b8;">
                    📄 <strong style="color:#e2e8f0;">{len(stats.get('sources',[]))}</strong> Documents
                </div>
                <div style="background:#131e35; border-radius:8px; padding:0.5rem 0.8rem;
                            font-size:0.82rem; color:#94a3b8;">
                    🧩 <strong style="color:#e2e8f0;">{stats.get('total_chunks',0)}</strong> Indexed Chunks
                </div>
                <div style="background:#131e35; border-radius:8px; padding:0.5rem 0.8rem;
                            font-size:0.82rem; color:#94a3b8;">
                    📚 <strong style="color:#e2e8f0;">{len(stats.get('subjects',[]))}</strong> Subjects
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # API Key status
        api_ok = bool(GOOGLE_API_KEY) if MODULES_OK else False
        if api_ok:
            st.markdown("""<div style="font-size:0.8rem; color:#10b981;">✅ Gemini API Connected</div>""",
                        unsafe_allow_html=True)
        else:
            st.markdown("""<div style="font-size:0.8rem; color:#f59e0b;">⚠️ API Key Missing</div>""",
                        unsafe_allow_html=True)

        # Clear chat
        if st.session_state.page == "chat" and st.session_state.chat_history:
            st.divider()
            if st.button("🗑️  Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()


# ─────────────────────────────────────────────────────────────────
#  Page: Home
# ─────────────────────────────────────────────────────────────────

def page_home():
    # Welcome Banner
    st.markdown("""
    <div class="welcome-banner animate-fade">
        <h2>Your AI-Powered Academic Companion</h2>
        <p>Upload your textbooks, lecture notes, lab manuals, and question papers. 
        Ask anything — get comprehensive, source-attributed answers in seconds.</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick action buttons
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("📁  Upload Documents", use_container_width=True, key="home_upload", on_click=set_page, args=("upload",))
    with c2:
        st.button("🧠  Start Chatting", use_container_width=True, key="home_chat", on_click=set_page, args=("chat",))
    with c3:
        st.button("📝  Solve Questions", use_container_width=True, key="home_qsolve", on_click=set_page, args=("questions",))

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature Cards
    st.markdown("""<div class="section-title">✨ What You Can Do</div>""", unsafe_allow_html=True)
    cols = st.columns(4)
    features = [
        ("📖", "Topic Explanation", "Ask to explain any topic. Get theory, examples, and key points drawn from your study materials.", "chat", "Open Chat ➔"),
        ("📝", "Question Solving", "Paste exam questions and get detailed, mark-ready answers using your uploaded content.", "questions", "Open Solver ➔"),
        ("🧠", "Quiz Generation", "Generate practice MCQs and short-answer questions from your uploaded materials.", "chat", "Generate Quiz ➔"),
        ("📊", "Study Dashboard", "Track which topics are covered, how many documents are indexed, and content breakdown.", "dashboard", "Open Dashboard ➔"),
    ]
    for col, (icon, title, desc, page_id, btn_label) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="feature-card" style="margin-bottom:0.8rem;">
                <div class="f-icon">{icon}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            st.button(btn_label, key=f"feat_btn_{page_id}_{title.split()[0].lower()}", use_container_width=True, on_click=set_page, args=(page_id,))

    st.markdown("<br>", unsafe_allow_html=True)

    # Supported formats
    st.markdown("""
    <div class="section-card animate-fade">
        <div class="section-title">📂 Supported Document Formats</div>
        <div style="display:flex; gap:1rem; flex-wrap:wrap;">
            <div style="background:#1a2540; border-radius:10px; padding:0.6rem 1.2rem; font-size:0.85rem; border:1px solid rgba(99,102,241,0.2);">
                <strong style="color:#818cf8;">📄 PDF</strong><br><span style="color:#64748b; font-size:0.75rem;">Textbooks, Question Papers</span>
            </div>
            <div style="background:#1a2540; border-radius:10px; padding:0.6rem 1.2rem; font-size:0.85rem; border:1px solid rgba(99,102,241,0.2);">
                <strong style="color:#818cf8;">📝 DOCX</strong><br><span style="color:#64748b; font-size:0.75rem;">Notes, Lab Manuals</span>
            </div>
            <div style="background:#1a2540; border-radius:10px; padding:0.6rem 1.2rem; font-size:0.85rem; border:1px solid rgba(99,102,241,0.2);">
                <strong style="color:#818cf8;">📊 PPTX</strong><br><span style="color:#64748b; font-size:0.75rem;">Lecture Slides</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Example queries
    st.markdown("""
    <div class="section-card animate-fade">
        <div class="section-title">💬 Example Queries</div>
        <div style="display:flex; flex-direction:column; gap:0.5rem;">
    """, unsafe_allow_html=True)

    examples = [
        ("📖", "Explain Database Normalization with examples"),
        ("🎯", "How to solve Q3 from the 2023 DBMS question paper?"),
        ("📝", "Generate 5 MCQs on Operating System Scheduling"),
        ("💡", "What are the key differences between TCP and UDP?"),
        ("🔬", "What is the procedure for Experiment 4 in the lab manual?"),
    ]
    for icon, ex in examples:
        st.markdown(f"""
        <div style="background:#1a2540; border:1px solid rgba(99,102,241,0.15); border-radius:10px;
                    padding:0.6rem 1rem; font-size:0.85rem; color:#94a3b8; cursor:pointer;
                    transition:all 0.2s; display:flex; align-items:center; gap:0.6rem;">
            <span>{icon}</span> <span>{ex}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # API Key Warning
    if MODULES_OK and not GOOGLE_API_KEY:
        st.markdown("""
        <div class="api-warning">
            ⚠️ <strong>Gemini API Key Not Set</strong><br>
            Copy <code>.env.example</code> → <code>.env</code> and add your key.<br>
            Get a <strong>free</strong> key at: <a href="https://aistudio.google.com/app/apikey" target="_blank">aistudio.google.com/app/apikey</a>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
#  Page: Upload Documents
# ─────────────────────────────────────────────────────────────────

def page_upload():
    st.markdown("""
    <div class="top-header animate-fade">
        <span class="header-logo">📁</span>
        <div>
            <h1>Upload Documents</h1>
            <div class="tagline">Add your study materials — PDFs, DOCX, PPTX supported</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not MODULES_OK:
        st.error(f"Module load error: {MODULE_ERROR}")
        return

    col_upload, col_library = st.columns([3, 2])

    with col_upload:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📤 Upload New Documents</div>', unsafe_allow_html=True)

        subject_input = st.text_input(
            "Subject Name",
            placeholder="e.g., DBMS, Operating Systems, Data Structures...",
            key="upload_subject",
        )

        uploaded_files = st.file_uploader(
            "Drag & drop or browse files",
            type=["pdf", "docx", "doc", "pptx", "ppt"],
            accept_multiple_files=True,
            key="file_uploader",
        )

        if uploaded_files and subject_input:
            if st.button("🚀  Index Documents", use_container_width=True, key="index_btn"):
                progress_bar = st.progress(0)
                status_text = st.empty()

                all_chunks = []
                for i, uploaded_file in enumerate(uploaded_files):
                    status_text.markdown(
                        f'<div class="animate-pulse" style="color:#94a3b8; font-size:0.85rem;">Processing: {uploaded_file.name}...</div>',
                        unsafe_allow_html=True,
                    )
                    # Save to temp file
                    suffix = Path(uploaded_file.name).suffix
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(uploaded_file.read())
                        tmp_path = tmp.name

                    try:
                        chunks = process_uploaded_file(tmp_path, subject_input)
                        all_chunks.extend(chunks)

                        # Record in session
                        ct = chunks[0].metadata.get("content_type", "textbook") if chunks else "textbook"
                        st.session_state.uploaded_docs.append({
                            "name": uploaded_file.name,
                            "subject": subject_input,
                            "content_type": ct,
                            "chunks": len(chunks),
                        })
                    except Exception as e:
                        st.warning(f"⚠️ Could not process {uploaded_file.name}: {e}")
                    finally:
                        os.unlink(tmp_path)

                    progress_bar.progress((i + 1) / len(uploaded_files))

                if all_chunks:
                    status_text.markdown(
                        '<div class="animate-pulse" style="color:#818cf8; font-size:0.85rem;">Embedding and indexing...</div>',
                        unsafe_allow_html=True,
                    )
                    try:
                        add_documents(all_chunks)
                        status_text.empty()
                        progress_bar.empty()
                        st.success(f"✅ Successfully indexed **{len(all_chunks)} chunks** from {len(uploaded_files)} file(s)!")
                        time.sleep(0.5)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Indexing error: {e}")
        elif uploaded_files and not subject_input:
            st.markdown("""
            <div style="background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3);
                        border-radius:8px; padding:0.7rem 1rem; font-size:0.85rem; color:#f59e0b;">
                ⚠️ Please enter a subject name before uploading.
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # API key reminder
        if not GOOGLE_API_KEY:
            st.markdown("""
            <div class="api-warning">
                ⚠️ <strong>API Key Required for Indexing</strong><br>
                Set <code>GOOGLE_API_KEY</code> in your <code>.env</code> file.<br>
                Free key: <a href="https://aistudio.google.com/app/apikey">aistudio.google.com</a>
            </div>
            """, unsafe_allow_html=True)

    with col_library:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📚 Indexed Library</div>', unsafe_allow_html=True)

        try:
            stats = get_collection_stats()
            sources = stats.get("sources", [])

            if not sources:
                st.markdown("""
                <div style="text-align:center; padding:2rem; color:#475569;">
                    <div style="font-size:2rem; margin-bottom:0.5rem;">📭</div>
                    <div>No documents indexed yet.<br>Upload your first document!</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Content type breakdown
                ct_counts = stats.get("content_types", {})
                ct_labels = {
                    "question_paper": "📝 Q-Papers",
                    "lab_manual": "🔬 Lab Manuals",
                    "lecture_notes": "📋 Lecture Notes",
                    "textbook": "📚 Textbooks",
                }
                total = sum(ct_counts.values()) or 1
                for ct, label in ct_labels.items():
                    count = ct_counts.get(ct, 0)
                    if count:
                        pct = int(count / total * 100)
                        st.markdown(f"""
                        <div style="margin-bottom:0.6rem;">
                            <div style="display:flex; justify-content:space-between; 
                                        font-size:0.8rem; color:#94a3b8; margin-bottom:3px;">
                                <span>{label}</span><span>{count} chunks ({pct}%)</span>
                            </div>
                        """, unsafe_allow_html=True)
                        st.progress(pct / 100)
                        st.markdown("</div>", unsafe_allow_html=True)

                st.divider()

                # Document list
                st.markdown(f'<div style="font-size:0.78rem; color:#64748b; margin-bottom:0.6rem;">📄 {len(sources)} Documents</div>', unsafe_allow_html=True)
                for src in sources:
                    # Find content type from session
                    ct = "textbook"
                    for d in st.session_state.uploaded_docs:
                        if d["name"] == src:
                            ct = d["content_type"]
                            break
                    st.markdown(f"""
                    <div class="doc-card">
                        <span style="font-size:1.2rem;">{get_content_type_emoji(ct)}</span>
                        <div style="flex:1; min-width:0;">
                            <div style="font-size:0.82rem; font-weight:500; color:#e2e8f0; 
                                        white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                                {src}
                            </div>
                            {ct_badge(ct)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Could not load library: {e}")

        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
#  Page: Chat Assistant
# ─────────────────────────────────────────────────────────────────

def page_chat():
    st.markdown("""
    <div class="top-header animate-fade">
        <span class="header-logo">🧠</span>
        <div>
            <h1>Chat Assistant</h1>
            <div class="tagline">Ask anything about your uploaded study materials</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not MODULES_OK:
        st.error(f"Module error: {MODULE_ERROR}")
        return

    has_docs = collection_exists_and_has_docs()

    if not has_docs:
        st.markdown("""
        <div style="text-align:center; padding:4rem 2rem; background:#131e35; 
                    border-radius:16px; border:1px solid rgba(99,102,241,0.2);">
            <div style="font-size:3rem; margin-bottom:1rem;">📭</div>
            <div style="font-family:'Space Grotesk',sans-serif; font-size:1.3rem; 
                        font-weight:600; color:#e2e8f0; margin-bottom:0.5rem;">
                No Documents Uploaded Yet
            </div>
            <div style="color:#64748b; font-size:0.9rem; margin-bottom:1.5rem;">
                Upload your study materials first to start asking questions.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("📁  Go to Upload", use_container_width=False, on_click=set_page, args=("upload",))
        return

    # Chat history display
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div style="text-align:center; padding:3rem 1rem; color:#475569;">
                <div style="font-size:2.5rem; margin-bottom:0.8rem;">💬</div>
                <div style="font-size:0.95rem;">Start by asking a question about your study materials.</div>
                <div style="font-size:0.8rem; margin-top:0.8rem; color:#374151;">
                    Try: "Explain Database Normalization" or "Solve Q5 from the 2023 paper"
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="msg-user">
                        <div class="bubble-user">{msg["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    qtype = msg.get("qtype", "topic_explanation")
                    st.markdown(f"""
                    <div class="msg-ai">
                        <div class="avatar-ai">🤖</div>
                        <div>
                            {qtype_badge_html(qtype)}
                            <div class="bubble-ai">{msg["content"]}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Source chips
                    docs = msg.get("docs", [])
                    if docs:
                        srcs = list({d.metadata.get("source", "?") for d in docs})
                        with st.expander(f"📂 {len(srcs)} source(s) used", expanded=False):
                            chips = "".join([f'<span class="source-chip">{s}</span>' for s in srcs])
                            st.markdown(f'<div style="margin-top:4px;">{chips}</div>', unsafe_allow_html=True)

    st.divider()

    # Chat input
    subject = st.session_state.active_subject
    if subject == "All Subjects":
        subject = None

    if user_input := st.chat_input("Ask about your study materials..."):
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "docs": [],
            "qtype": "",
        })
        st.rerun()

    # Process last user message if not yet answered
    history = st.session_state.chat_history
    if history and history[-1]["role"] == "user" and not GOOGLE_API_KEY:
        st.markdown("""
        <div class="api-warning">
            ⚠️ <strong>API Key Missing!</strong> Set <code>GOOGLE_API_KEY</code> in <code>.env</code> to enable AI responses.
        </div>
        """, unsafe_allow_html=True)
    elif history and history[-1]["role"] == "user":
        user_msg = history[-1]["content"]
        prev_history = [h for h in history[:-1] if h["role"] in ("user", "assistant")]

        # Show typing indicator
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="msg-ai" style="margin-top:1rem;">
            <div class="avatar-ai">🤖</div>
            <div class="bubble-ai">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        answer, docs, qtype = chat(
            user_query=user_msg,
            chat_history=prev_history,
            subject_filter=subject,
        )

        typing_placeholder.empty()

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "docs": docs,
            "qtype": qtype,
        })
        st.rerun()


# ─────────────────────────────────────────────────────────────────
#  Page: Question Solver
# ─────────────────────────────────────────────────────────────────

def page_question_solver():
    st.markdown("""
    <div class="top-header animate-fade">
        <span class="header-logo">📝</span>
        <div>
            <h1>Question Solver</h1>
            <div class="tagline">Paste exam questions and get detailed, step-by-step answers</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not MODULES_OK:
        st.error(f"Module error: {MODULE_ERROR}")
        return

    has_docs = collection_exists_and_has_docs()

    col_input, col_output = st.columns([2, 3])

    with col_input:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎯 Enter Your Question</div>', unsafe_allow_html=True)

        # Pre-populate from example buttons (avoids StreamlitAPIException)
        _pending = st.session_state.pop("_question_pending", None)
        if _pending is not None:
            st.session_state.pop("question_input", None)   # reset so value= takes effect

        question_text = st.text_area(
            "Paste your exam question here",
            value=_pending or "",
            placeholder="e.g., Q.3 (a) Explain the concept of Deadlock with necessary conditions. (10 marks)\n\nor: How to solve the Banker's Algorithm for deadlock avoidance?",
            height=180,
            key="question_input",
        )

        context_hint = st.text_input(
            "Additional Context (optional)",
            placeholder="e.g., 2023 OS exam, Unit 3...",
            key="context_hint",
        )

        subject = st.session_state.active_subject
        if subject == "All Subjects":
            subject = None

        solve_btn = st.button("✅  Solve This Question", use_container_width=True, key="solve_btn",
                              disabled=not (question_text.strip() and has_docs))

        if not has_docs:
            st.markdown("""
            <div style="background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3);
                        border-radius:8px; padding:0.7rem; font-size:0.82rem; color:#f59e0b; margin-top:0.5rem;">
                ⚠️ Upload documents first to use the question solver.
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Quick examples
        st.markdown('<div style="font-size:0.78rem; color:#64748b; margin-bottom:0.5rem; text-transform:uppercase; letter-spacing:0.05em;">Quick Examples</div>', unsafe_allow_html=True)
        examples = [
            "Explain the difference between process and thread with examples.",
            "What is normalization? Explain 1NF, 2NF, and 3NF with examples.",
            "Describe the working of a Binary Search Tree with insertion and deletion.",
            "Explain TCP 3-way handshake with a diagram.",
        ]
        for ex in examples:
            st.button(
                f"💬 {ex[:45]}...",
                key=f"qex_{hash(ex)}",
                use_container_width=True,
                on_click=set_question_pending,
                args=(ex,),
            )

        st.markdown('</div>', unsafe_allow_html=True)

    with col_output:
        st.markdown('<div class="section-card" style="min-height:500px;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 Answer</div>', unsafe_allow_html=True)

        if "qsolver_result" not in st.session_state:
            st.markdown("""
            <div style="text-align:center; padding:4rem 1rem; color:#475569;">
                <div style="font-size:2.5rem; margin-bottom:0.8rem;">💡</div>
                <div style="font-size:0.9rem;">Your answer will appear here.</div>
                <div style="font-size:0.8rem; margin-top:0.5rem; color:#374151;">
                    Enter a question and click "Solve"
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            result = st.session_state.qsolver_result
            st.markdown(result["answer"])
            st.divider()
            if result["docs"]:
                srcs = list({d.metadata.get("source", "?") for d in result["docs"]})
                chips = "".join([f'<span class="source-chip">{s}</span>' for s in srcs])
                st.markdown(f'<div><strong style="font-size:0.8rem; color:#64748b;">📂 Sources:</strong><br>{chips}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Handle solve
    if solve_btn and question_text.strip():
        full_query = question_text.strip()
        if context_hint:
            full_query = f"{full_query}\n[Context: {context_hint}]"

        with st.spinner("🤔 Generating detailed answer..."):
            answer, docs, qtype = chat(
                user_query=full_query,
                chat_history=[],
                subject_filter=subject,
            )

        st.session_state.qsolver_result = {"answer": answer, "docs": docs, "qtype": qtype}
        st.rerun()


# ─────────────────────────────────────────────────────────────────
#  Page: Dashboard
# ─────────────────────────────────────────────────────────────────

def page_dashboard():
    st.markdown("""
    <div class="top-header animate-fade">
        <span class="header-logo">📊</span>
        <div>
            <h1>Subject Dashboard</h1>
            <div class="tagline">Overview of your indexed academic content</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not MODULES_OK:
        st.error(f"Module error: {MODULE_ERROR}")
        return

    try:
        stats = get_collection_stats()
    except Exception as e:
        st.error(f"Could not load stats: {e}")
        return

    total_chunks = stats.get("total_chunks", 0)
    sources = stats.get("sources", [])
    subjects = stats.get("subjects", [])
    ct_counts = stats.get("content_types", {})

    if total_chunks == 0:
        st.markdown("""
        <div style="text-align:center; padding:5rem; background:#131e35;
                    border-radius:16px; border:1px solid rgba(99,102,241,0.2);">
            <div style="font-size:3rem; margin-bottom:1rem;">📭</div>
            <div style="font-size:1.2rem; color:#e2e8f0; margin-bottom:0.5rem;">No Content Indexed Yet</div>
            <div style="color:#64748b; font-size:0.9rem;">Upload documents to see your dashboard</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Stat Cards ──
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("📄", len(sources), "Documents", c1),
        ("🧩", total_chunks, "Text Chunks", c2),
        ("📚", len(subjects), "Subjects", c3),
        ("🗂️", len(ct_counts), "Content Types", c4),
    ]
    for icon, val, label, col in cards:
        with col:
            st.markdown(f"""
            <div class="stat-card animate-fade">
                <div class="stat-icon">{icon}</div>
                <div class="stat-value">{val}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Content Type Breakdown ──
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Content Type Breakdown</div>', unsafe_allow_html=True)

        ct_labels = {
            "question_paper": ("📝 Question Papers", "var(--amber)"),
            "lab_manual":     ("🔬 Lab Manuals",     "var(--teal)"),
            "lecture_notes":  ("📋 Lecture Notes",    "var(--accent2)"),
            "textbook":       ("📚 Textbooks",         "var(--green)"),
        }
        total = sum(ct_counts.values()) or 1
        for ct, (label, color) in ct_labels.items():
            count = ct_counts.get(ct, 0)
            pct = count / total
            st.markdown(f"""
            <div style="margin-bottom:1rem;">
                <div style="display:flex; justify-content:space-between; 
                            font-size:0.85rem; margin-bottom:4px;">
                    <span style="color:#e2e8f0;">{label}</span>
                    <span style="color:#64748b;">{count} chunks ({int(pct*100)}%)</span>
                </div>
            """, unsafe_allow_html=True)
            st.progress(pct)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📚 Subjects Indexed</div>', unsafe_allow_html=True)

        if subjects:
            for sub in subjects:
                st.markdown(f"""
                <div style="background:#1a2540; border-radius:10px; padding:0.7rem 1rem;
                            margin-bottom:0.5rem; border:1px solid rgba(99,102,241,0.15);
                            display:flex; align-items:center; gap:0.6rem;">
                    <span style="font-size:1.1rem;">📘</span>
                    <span style="font-size:0.88rem; color:#e2e8f0; font-weight:500;">{sub}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#64748b; font-size:0.9rem;">No subjects found.</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Document List ──
    st.markdown('<div class="section-card animate-fade">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">📄 All Indexed Documents ({len(sources)})</div>', unsafe_allow_html=True)

    for src in sources:
        ct = "textbook"
        chunks = 0
        subject = "—"
        for d in st.session_state.uploaded_docs:
            if d["name"] == src:
                ct = d.get("content_type", "textbook")
                chunks = d.get("chunks", 0)
                subject = d.get("subject", "—")
                break

        cols = st.columns([0.05, 0.45, 0.2, 0.15, 0.15])
        with cols[0]:
            st.markdown(f'<div style="font-size:1.2rem;">{get_content_type_emoji(ct)}</div>', unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f'<div style="font-size:0.85rem; color:#e2e8f0; font-weight:500; padding-top:4px;">{src}</div>', unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f'<div style="font-size:0.82rem; color:#94a3b8; padding-top:4px;">📚 {subject}</div>', unsafe_allow_html=True)
        with cols[3]:
            st.markdown(f'<div style="font-size:0.82rem; color:#64748b; padding-top:4px;">🧩 {chunks} chunks</div>', unsafe_allow_html=True)
        with cols[4]:
            st.markdown(ct_badge(ct), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Quick Topic Summary ──
    st.markdown('<div class="section-card animate-fade">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ Quick Topic Summary</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.85rem; color:#94a3b8; margin-bottom:0.8rem;">Generate a quick revision summary for any topic from your materials</div>', unsafe_allow_html=True)

    col_topic, col_btn = st.columns([4, 1])
    with col_topic:
        topic_input = st.text_input("", placeholder="Enter a topic name...", key="topic_summary_input", label_visibility="collapsed")
    with col_btn:
        if st.button("⚡ Generate", key="topic_sum_btn", use_container_width=True):
            if topic_input:
                with st.spinner("Generating summary..."):
                    summary = get_topic_summary(topic_input, st.session_state.active_subject if st.session_state.active_subject != "All Subjects" else None)
                st.session_state["topic_summary_result"] = summary

    if "topic_summary_result" in st.session_state:
        st.markdown(f"""
        <div style="background:#1a2540; border:1px solid rgba(99,102,241,0.2);
                    border-radius:12px; padding:1.2rem; font-size:0.88rem; 
                    color:#e2e8f0; line-height:1.7; margin-top:0.8rem;">
            {st.session_state.topic_summary_result}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
#  Main App Router
# ─────────────────────────────────────────────────────────────────

def main():
    render_sidebar()

    if not MODULES_OK:
        st.error(f"⚠️ Failed to load application modules: {MODULE_ERROR}")
        st.info("Run: `pip install -r requirements.txt` to install all dependencies.")
        return

    page = st.session_state.page
    if page == "home":
        page_home()
    elif page == "upload":
        page_upload()
    elif page == "chat":
        page_chat()
    elif page == "questions":
        page_question_solver()
    elif page == "dashboard":
        page_dashboard()
    else:
        page_home()


if __name__ == "__main__":
    main()
