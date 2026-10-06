"""
ChromaDB Vector Store Manager
------------------------------
Handles embedding, indexing, and semantic search of academic documents.
Uses Google's embedding-001 model (free, same API key as Gemini).
"""

from __future__ import annotations

import os
from typing import List, Dict, Any, Optional

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import GOOGLE_API_KEY, EMBEDDING_MODEL, CHROMA_DB_PATH, RETRIEVAL_K


def _get_embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY,
    )


def get_or_create_vectorstore(collection_name: str = "academic_docs") -> Chroma:
    """Return an existing ChromaDB collection or create a new one."""
    embeddings = _get_embeddings()
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_PATH,
    )


def add_documents(
    docs: List[Document],
    collection_name: str = "academic_docs",
) -> Chroma:
    """Embed and add documents to the vector store."""
    embeddings = _get_embeddings()
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_PATH,
    )
    vectorstore.add_documents(docs)
    return vectorstore


def search_documents(
    query: str,
    collection_name: str = "academic_docs",
    k: int = RETRIEVAL_K,
    subject_filter: Optional[str] = None,
) -> List[Document]:
    """Semantic search with optional subject filter."""
    vectorstore = get_or_create_vectorstore(collection_name)

    where_filter: Optional[Dict] = None
    if subject_filter and subject_filter.lower() != "all subjects":
        where_filter = {"subject": {"$eq": subject_filter}}

    try:
        if where_filter:
            results = vectorstore.similarity_search(query, k=k, filter=where_filter)
        else:
            results = vectorstore.similarity_search(query, k=k)
    except Exception:
        results = vectorstore.similarity_search(query, k=k)

    return results


def get_collection_stats(collection_name: str = "academic_docs") -> Dict[str, Any]:
    """Return stats about stored documents."""
    try:
        vectorstore = get_or_create_vectorstore(collection_name)
        collection = vectorstore._collection
        count = collection.count()

        # Get unique sources and subjects
        if count == 0:
            return {"total_chunks": 0, "sources": [], "subjects": [], "content_types": {}}

        all_meta = collection.get(include=["metadatas"])["metadatas"] or []
        sources = list({m.get("source", "unknown") for m in all_meta if m})
        subjects = list({m.get("subject", "General") for m in all_meta if m})

        content_type_counts: Dict[str, int] = {}
        for m in all_meta:
            if m:
                ct = m.get("content_type", "unknown")
                content_type_counts[ct] = content_type_counts.get(ct, 0) + 1

        return {
            "total_chunks": count,
            "sources": sorted(sources),
            "subjects": sorted(subjects),
            "content_types": content_type_counts,
        }
    except Exception as e:
        return {"total_chunks": 0, "sources": [], "subjects": [], "content_types": {}, "error": str(e)}


def delete_document(source_filename: str, collection_name: str = "academic_docs") -> int:
    """Delete all chunks for a given source document. Returns number of deleted chunks."""
    try:
        vectorstore = get_or_create_vectorstore(collection_name)
        collection = vectorstore._collection
        results = collection.get(where={"source": {"$eq": source_filename}})
        ids_to_delete = results.get("ids", [])
        if ids_to_delete:
            collection.delete(ids=ids_to_delete)
        return len(ids_to_delete)
    except Exception:
        return 0


def collection_exists_and_has_docs(collection_name: str = "academic_docs") -> bool:
    """Check if the collection has at least one document."""
    stats = get_collection_stats(collection_name)
    return stats.get("total_chunks", 0) > 0
