import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── API ──────────────────────────────────────────────────────
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

# ── Models ───────────────────────────────────────────────────
LLM_MODEL: str = "gemini-2.5-flash"
EMBEDDING_MODEL: str = "models/gemini-embedding-001"

# ── Paths ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DB_PATH: str = str(BASE_DIR / "data" / "chroma_db")
UPLOADS_PATH: str = str(BASE_DIR / "data" / "uploads")

# ── RAG ──────────────────────────────────────────────────────
CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 200
RETRIEVAL_K: int = 6

# ── Ensure directories exist ─────────────────────────────────
os.makedirs(CHROMA_DB_PATH, exist_ok=True)
os.makedirs(UPLOADS_PATH, exist_ok=True)
