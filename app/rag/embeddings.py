"""
app/rag/embeddings.py
──────────────────────
Singleton embedding model using fastembed (ONNX-based, no PyTorch).
Runs on ~150MB RAM — suitable for free-tier cloud deployments.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import List

from langchain_community.embeddings import FastEmbedEmbeddings

logger = logging.getLogger("digital_finance_agent.embeddings")

# Multilingual model that fits in 512MB RAM (ONNX, no torch)
_FASTEMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> FastEmbedEmbeddings:
    """Return the cached multilingual fastembed embeddings model."""
    logger.info("Loading embedding model (fastembed): %s", _FASTEMBED_MODEL)
    model = FastEmbedEmbeddings(model_name=_FASTEMBED_MODEL)
    logger.info("Embedding model loaded successfully.")
    return model


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of text strings and return their vectors."""
    return get_embedding_model().embed_documents(texts)


def embed_query(query: str) -> List[float]:
    """Embed a single query string."""
    return get_embedding_model().embed_query(query)
