# Capabl-AI_Aivengers_Project

# 📚 AcademicAI — Subject Guide & Question Bank Assistant

> An AI-powered academic companion that turns your study materials into a comprehensive, conversational learning assistant.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-green?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini%202.5%20Flash-Free-yellow?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Persistent-purple?style=flat-square)

---

## 🌟 Features

| Feature | Description |
|---|---|
| 📁 **Multi-Format Upload** | PDF, DOCX, PPTX — auto-classified as Textbook, Q-Paper, Lab Manual, or Lecture Notes |
| 🧠 **AI Chat Assistant** | Ask anything about your uploaded materials using RAG (Retrieval-Augmented Generation) |
| 📝 **Question Solver** | Paste exam questions and get detailed, step-by-step answers with source attribution |
| 🎯 **Auto Query Routing** | Automatically detects if you're asking for a topic explanation, exam solution, or quiz |
| 📊 **Subject Dashboard** | Track indexed documents, content types, and quick topic summaries |
| 🔗 **Source Attribution** | Every answer cites which documents it drew from |

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/academicai.git
cd academicai
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Your API Key
```bash
# Copy the example env file
cp .env.example .env
```
Then open `.env` and add your **free** Gemini API key:
```
GOOGLE_API_KEY=your_key_here
```
> 🔑 Get a **free** key at: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
> - Free tier: **1,500 requests/day**, **1M tokens/min** — very generous!

### 5. Run the App
```bash
streamlit run main.py
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│         Streamlit UI  (main.py)                 │
│  Home | Upload | Chat | Q-Solver | Dashboard    │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│          Agent Core  (app/agent/agent_core.py)  │
│  Query Classifier → Prompt Router → Gemini LLM  │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│       ChromaDB Vector Store                     │
│  (app/vector_store/chroma_store.py)             │
│  Google embedding-001 → Semantic Search         │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│       Document Processors                       │
│  (app/document_processing/processors.py)        │
│  PDF (PyMuPDF) | DOCX | PPTX + Auto-Classifier  │
└─────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
AcademicAI/
├── main.py                          # 🎨 Streamlit app entry point
├── requirements.txt                 # 📦 Dependencies
├── .env.example                     # 🔑 API key template
├── .env                             # 🔑 Your actual API key (not committed)
├── .gitignore
├── .streamlit/
│   └── config.toml                  # 🎨 Dark theme config
├── app/
│   ├── config.py                    # ⚙️  Configuration & paths
│   ├── document_processing/
│   │   └── processors.py           # 📄 PDF/DOCX/PPTX processing + classifier
│   ├── vector_store/
│   │   └── chroma_store.py         # 🗄️  ChromaDB vector store operations
│   └── agent/
│       └── agent_core.py           # 🤖 LangChain + Gemini AI agent
└── data/
    ├── uploads/                     # 📁 Temporary upload storage
    └── chroma_db/                   # 🗄️  Persistent vector database
```

---

## 🎓 How to Use

### Upload Documents
1. Go to **📁 Upload Documents**
2. Enter your **Subject Name** (e.g., "DBMS", "Operating Systems")
3. Upload one or more files (PDF, DOCX, PPTX)
4. Click **🚀 Index Documents** — the AI will process and embed them

### Chat with Your Materials
1. Go to **🧠 Chat Assistant**
2. Ask questions naturally:
   - *"Explain Database Normalization with examples"*
   - *"What are the key scheduling algorithms in OS?"*
   - *"Summarize Unit 3 from my notes"*

### Solve Exam Questions
1. Go to **📝 Question Solver**
2. Paste your exam question
3. Get a complete, structured answer with source citations

### Generate Practice Quizzes
In the **Chat Assistant**, ask:
- *"Generate 5 MCQs on SQL joins"*
- *"Test me on Operating System concepts"*
- *"Give me practice questions from Unit 2"*

---

## 🔧 Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | Streamlit + Custom CSS |
| **LLM** | Google Gemini 2.5 Flash (Free API) |
| **Embeddings** | Google gemini-embedding-001 (Free API) |
| **Vector DB** | ChromaDB (Persistent Local) |
| **Framework** | LangChain |
| **PDF Processing** | PyMuPDF (fitz) |
| **DOCX Processing** | python-docx |
| **PPTX Processing** | python-pptx |

---

## 🌐 Deploy to Streamlit Cloud

1. Push your code to a **public GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set `main.py` as the entry point
4. Add `GOOGLE_API_KEY` in **Secrets** (Settings → Secrets):
   ```toml
   GOOGLE_API_KEY = "your_key_here"
   ```
5. Click **Deploy** — your app will be live with a public URL!

> ⚠️ **Note:** ChromaDB data is ephemeral on Streamlit Cloud (resets on restart). For production, consider switching to Pinecone or a hosted vector DB.

---

## 📖 Academic Content Types Detected

| Type | Detection Signals | Icon |
|---|---|---|
| **Question Paper** | "Q.1", "marks", year patterns, "answer any" | 📝 |
| **Lab Manual** | "Experiment No.", "Aim:", "Procedure:", "Observation:" | 🔬 |
| **Lecture Notes** | "Lecture N", "Unit", bullet-point heavy content | 📋 |
| **Textbook** | Long paragraphs, chapter structure (default) | 📚 |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push and open a Pull Request

---

## 📄 License

MIT License — free to use for academic and personal projects.

---

## 🙏 Acknowledgments

Built with ❤️ for the **Capabl AI Project** — Academic Learning Track A.
Powered by Google Gemini, LangChain, ChromaDB, and Streamlit.
