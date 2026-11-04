"""
app/rag/embeddings.py
──────────────────────
Singleton embedding model using sentence-transformers (multilingual).
No API key required — runs locally.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import List

from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings

logger = logging.getLogger("digital_finance_agent.embeddings")


@lru_cache(maxsize=1)
def get_embedding_model() -> HuggingFaceEmbeddings:
    """Return the cached multilingual sentence-transformer embeddings model."""
    logger.info("Loading embedding model: %s", settings.embedding_model)
    model = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    logger.info("Embedding model loaded successfully.")
    return model


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of text strings and return their vectors."""
    return get_embedding_model().embed_documents(texts)


def embed_query(query: str) -> List[float]:
    """Embed a single query string."""
    return get_embedding_model().embed_query(query)
