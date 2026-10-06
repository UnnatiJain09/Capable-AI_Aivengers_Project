"""
AI Agent Core
--------------
LangChain-powered academic assistant using Google Gemini 1.5 Flash.
Supports topic explanation, question solving, and content synthesis
with conversational memory and source attribution.
"""

from __future__ import annotations

import re
from typing import List, Dict, Any, Optional, Tuple

from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.config import GOOGLE_API_KEY, LLM_MODEL
from app.vector_store.chroma_store import search_documents


# ─────────────────────────────────────────────────────────────────
#  LLM Setup
# ─────────────────────────────────────────────────────────────────

def get_llm(temperature: float = 0.3) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=temperature,
        convert_system_message_to_human=True,
    )


# ─────────────────────────────────────────────────────────────────
#  Query Type Classifier
# ─────────────────────────────────────────────────────────────────

_QUESTION_SOLVER_PATTERNS = [
    r"\bQ\s*\.?\s*\d+\b",
    r"\b(solve|solving|solution to|answer to)\b",
    r"\b(20\d{2}|19\d{2})\s*(exam|paper|question|q\.?)\b",
    r"\bfrom\s+the\s+(question\s+)?paper\b",
    r"\bhow\s+to\s+(solve|answer)\b",
    r"\bmark[s]?\s+question\b",
    r"\bprevious\s+year\b",
]

_QUIZ_PATTERNS = [
    r"\b(quiz|test\s+me|practice\s+q(uestion)?s?|mcq|multiple\s+choice)\b",
    r"\bgive\s+me\s+(some\s+)?(question|quiz|practice)\b",
    r"\bgenerate\s+(question|quiz|mcq)\b",
]

def classify_query(query: str) -> str:
    """Returns: 'question_solver' | 'quiz' | 'topic_explanation'"""
    q = query.lower()
    for p in _QUESTION_SOLVER_PATTERNS:
        if re.search(p, q, re.I):
            return "question_solver"
    for p in _QUIZ_PATTERNS:
        if re.search(p, q, re.I):
            return "quiz"
    return "topic_explanation"


# ─────────────────────────────────────────────────────────────────
#  Prompt Templates
# ─────────────────────────────────────────────────────────────────

SYSTEM_BASE = """You are **AcademicAI**, an intelligent subject guide and question bank assistant.
You help students understand topics by synthesizing information from their uploaded study materials.
Always be thorough, educational, and cite the source documents used.
If the uploaded materials don't contain enough information, clearly say so and provide a general academic answer."""

TOPIC_PROMPT_TEMPLATE = """{system}

📚 **Context from uploaded study materials:**
{context}

🗂️ **Conversation so far:**
{chat_history}

🎓 **Student's question:** {question}

Provide a comprehensive educational response structured as follows:

## 📖 Theory & Concepts
[Core explanation of the topic]

## 💡 Key Points
[Bullet points of the most important concepts]

## 🔍 Examples
[Practical examples from the study materials if available]

## 📝 Practice Questions
[2-3 relevant practice questions on this topic]

## 📂 Sources Used
[List the document names you drew from]"""

QUESTION_SOLVER_TEMPLATE = """{system}

📚 **Context from uploaded study materials:**
{context}

🗂️ **Conversation so far:**
{chat_history}

🎯 **Exam question to solve:** {question}

Provide a complete exam-ready answer structured as:

## 🎯 Question Analysis
[What the question is asking and which topic it covers]

## 📚 Relevant Concepts & Theory
[Key definitions, theorems, formulas needed]

## ✅ Step-by-Step Answer
[Detailed, mark-worthy solution]

## 💬 Key Takeaway
[What to remember for the exam]

## 📂 Sources Used
[Documents referenced]"""

QUIZ_TEMPLATE = """{system}

📚 **Context from uploaded study materials:**
{context}

🗂️ **Conversation so far:**
{chat_history}

📝 **Request:** {question}

Generate a well-structured practice quiz from the uploaded materials:

## 📝 Practice Quiz

[Generate 5 questions mix of MCQ, short answer, and long answer.
For MCQs: provide 4 options and mark the correct one.
For short/long: provide the model answer below each question.]

## 📂 Topics Covered
[Which topics/chapters these questions are from]"""


# ─────────────────────────────────────────────────────────────────
#  Core Chat Function
# ─────────────────────────────────────────────────────────────────

def format_chat_history(history: List[Dict[str, str]]) -> str:
    """Convert list of {role, content} dicts to readable string."""
    if not history:
        return "No previous conversation."
    lines = []
    for msg in history[-6:]:  # Keep last 6 turns for context
        role = "Student" if msg["role"] == "user" else "AcademicAI"
        lines.append(f"{role}: {msg['content'][:400]}")
    return "\n".join(lines)


def format_context(docs: List[Document]) -> str:
    """Format retrieved documents into a readable context block."""
    if not docs:
        return "No relevant content found in uploaded documents."
    parts = []
    for i, doc in enumerate(docs, 1):
        meta = doc.metadata
        src = meta.get("source", "Unknown")
        ct = meta.get("content_type", "document")
        pg = meta.get("page", "")
        header = f"[Source {i}: {src} | Type: {ct} | Page: {pg}]"
        parts.append(f"{header}\n{doc.page_content.strip()}")
    return "\n\n---\n\n".join(parts)


def chat(
    user_query: str,
    chat_history: List[Dict[str, str]],
    subject_filter: Optional[str] = None,
) -> Tuple[str, List[Document], str]:
    """
    Main chat function.

    Returns:
        (answer_text, source_documents, query_type)
    """
    if not GOOGLE_API_KEY:
        return (
            "⚠️ **API Key Missing!** Please add your `GOOGLE_API_KEY` in the `.env` file.\n\n"
            "Get a free key at: https://aistudio.google.com/app/apikey",
            [],
            "error",
        )

    # 1. Classify query type
    query_type = classify_query(user_query)

    # 2. Retrieve relevant documents
    try:
        docs = search_documents(user_query, subject_filter=subject_filter)
    except Exception as e:
        docs = []

    # 3. Format inputs
    context = format_context(docs)
    history_str = format_chat_history(chat_history)

    # 4. Select prompt
    if query_type == "question_solver":
        prompt_str = QUESTION_SOLVER_TEMPLATE
    elif query_type == "quiz":
        prompt_str = QUIZ_TEMPLATE
    else:
        prompt_str = TOPIC_PROMPT_TEMPLATE

    final_prompt = prompt_str.format(
        system=SYSTEM_BASE,
        context=context,
        chat_history=history_str,
        question=user_query,
    )

    # 5. Call LLM
    llm = get_llm()
    try:
        response = llm.invoke([HumanMessage(content=final_prompt)])
        answer = response.content
    except Exception as e:
        answer = f"⚠️ **Error from Gemini:** {str(e)}\n\nPlease check your API key and try again."

    return answer, docs, query_type


def get_topic_summary(topic: str, subject_filter: Optional[str] = None) -> str:
    """Generate a concise topic summary card."""
    if not GOOGLE_API_KEY:
        return "API key missing."

    docs = search_documents(topic, subject_filter=subject_filter, k=4)
    context = format_context(docs)

    prompt = f"""{SYSTEM_BASE}

Context: {context}

Generate a concise 150-word summary of "{topic}" suitable for quick revision. 
Include: definition, 2-3 key points, and one example. No headers needed."""

    llm = get_llm(temperature=0.2)
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"
