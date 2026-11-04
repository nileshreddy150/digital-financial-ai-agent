"""
app/rag/vectorstore.py
───────────────────────
ChromaDB-backed persistent vector store.
Handles document ingestion, chunking, and similarity retrieval.
"""

from __future__ import annotations

import logging
import os
from typing import List, Dict, Any, Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from app.core.config import settings
from app.rag.embeddings import get_embedding_model
from app.rag.knowledge_base import FINANCIAL_DOCUMENTS

logger = logging.getLogger("digital_finance_agent.vectorstore")

_COLLECTION_NAME = "financial_literacy"
_vectorstore: Optional[Chroma] = None


def _build_documents() -> List[Document]:
    """Convert the knowledge-base dicts to LangChain Document objects."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    docs: List[Document] = []
    for entry in FINANCIAL_DOCUMENTS:
        chunks = splitter.split_text(entry["content"])
        for i, chunk in enumerate(chunks):
            docs.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "id": f"{entry['id']}_chunk{i}",
                        "title": entry["title"],
                        "category": entry["category"],
                        "source": entry["source"],
                        "language": entry["language"],
                    },
                )
            )
    logger.info("Built %d document chunks from knowledge base.", len(docs))
    return docs


def _is_vectorstore_populated(store: Chroma) -> bool:
    """Check whether the vector store already contains data."""
    try:
        return store._collection.count() > 0
    except Exception:
        return False


def get_vectorstore() -> Chroma:
    """Return the singleton Chroma vector store, initialising it if needed."""
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore

    persist_dir = os.path.abspath(settings.vectorstore_dir)
    os.makedirs(persist_dir, exist_ok=True)

    embedding_fn = get_embedding_model()

    store = Chroma(
        collection_name=_COLLECTION_NAME,
        embedding_function=embedding_fn,
        persist_directory=persist_dir,
    )

    if not _is_vectorstore_populated(store):
        logger.info("Vector store is empty — ingesting knowledge base …")
        docs = _build_documents()
        store.add_documents(docs)
        logger.info("Ingestion complete: %d chunks stored.", len(docs))
    else:
        count = store._collection.count()
        logger.info("Vector store loaded with %d existing chunks.", count)

    _vectorstore = store
    return _vectorstore


def similarity_search(
    query: str,
    k: int = None,
    filter_category: Optional[str] = None,
) -> List[Document]:
    """
    Retrieve the top-k most relevant documents for `query`.

    Args:
        query:           The user's question (any language — embedding is multilingual).
        k:               Number of results. Defaults to settings.top_k_results.
        filter_category: Optional Chroma metadata filter on 'category'.

    Returns:
        List of LangChain Document objects with page_content and metadata.
    """
    k = k or settings.top_k_results
    store = get_vectorstore()

    where = {"category": filter_category} if filter_category else None

    try:
        if where:
            results = store.similarity_search(query, k=k, filter=where)
        else:
            results = store.similarity_search(query, k=k)
        logger.debug("Retrieved %d chunks for query: %s", len(results), query[:80])
        return results
    except Exception as exc:
        logger.error("Vector store retrieval failed: %s", exc, exc_info=True)
        return []


def add_document(
    content: str,
    metadata: Dict[str, Any],
) -> None:
    """Add a single document to the vector store (for runtime expansion)."""
    store = get_vectorstore()
    doc = Document(page_content=content, metadata=metadata)
    store.add_documents([doc])
    logger.info("Added document to vector store: %s", metadata.get("title", "unknown"))
