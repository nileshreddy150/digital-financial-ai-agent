"""
app/rag/embeddings.py
──────────────────────
Embeddings via IBM watsonx.ai API.
Zero local RAM — all inference runs on IBM Cloud.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import List

from langchain_core.embeddings import Embeddings

from app.core.config import settings

logger = logging.getLogger("digital_finance_agent.embeddings")


class WatsonxEmbeddings(Embeddings):
    """Calls the IBM watsonx.ai embeddings API. No local model download."""

    def _embed(self, texts: List[str]) -> List[List[float]]:
        from ibm_watsonx_ai import Credentials
        from ibm_watsonx_ai.foundation_models import Embeddings as WxEmbeddings

        credentials = Credentials(
            url=settings.ibm_watsonx_url,
            api_key=settings.ibm_watsonx_api_key,
        )
        wx = WxEmbeddings(
            model_id=settings.ibm_watsonx_embedding_model_id,
            credentials=credentials,
            project_id=settings.ibm_watsonx_project_id,
        )
        response = wx.embed_documents(texts)
        return response

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        logger.debug("Embedding %d documents via watsonx.ai", len(texts))
        return self._embed(texts)

    def embed_query(self, text: str) -> List[float]:
        logger.debug("Embedding query via watsonx.ai")
        return self._embed([text])[0]


@lru_cache(maxsize=1)
def get_embedding_model() -> WatsonxEmbeddings:
    """Return the cached watsonx.ai embeddings instance."""
    logger.info(
        "Using IBM watsonx.ai embeddings: %s",
        settings.ibm_watsonx_embedding_model_id,
    )
    return WatsonxEmbeddings()


def embed_texts(texts: List[str]) -> List[List[float]]:
    return get_embedding_model().embed_documents(texts)


def embed_query(query: str) -> List[float]:
    return get_embedding_model().embed_query(query)
