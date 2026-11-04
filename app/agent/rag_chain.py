"""
app/agent/rag_chain.py
───────────────────────
Core RAG pipeline: retrieves relevant context from ChromaDB,
builds the prompt, and calls IBM Granite to generate an answer.

Flow:
  User query (any language)
    → detect & translate to English
    → condense follow-up question (if history present)
    → similarity search ChromaDB
    → build prompt with context + history
    → IBM Granite generates answer
    → translate response back to user language
    → return structured ChatResponse
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from langchain_classic.chains import LLMChain
from app.agent.granite_llm import get_granite_llm
from app.agent.prompts import (
    RAG_PROMPT,
    CONDENSE_QUESTION_PROMPT,
    SYSTEM_PROMPT,
)
from app.i18n.translator import (
    translate_query_to_english,
    translate_response_to_user_lang,
)
from app.rag.vectorstore import similarity_search
from app.core.config import settings

logger = logging.getLogger("digital_finance_agent.rag_chain")


@dataclass
class ChatMessage:
    role: str  # "user" | "assistant"
    content: str


@dataclass
class ChatResponse:
    answer: str
    sources: List[dict]
    detected_language: str
    english_query: str
    category_hint: Optional[str] = None


def _format_chat_history(history: List[ChatMessage]) -> str:
    """Format conversation history for the prompt."""
    if not history:
        return "No previous conversation."
    lines = []
    for msg in history[-6:]:  # keep last 3 exchanges (6 messages) to avoid context overflow
        role = "Human" if msg.role == "user" else "Assistant"
        lines.append(f"{role}: {msg.content}")
    return "\n".join(lines)


def _format_context(docs) -> str:
    """Format retrieved documents into a readable context block."""
    if not docs:
        return "No specific information found in the knowledge base for this query."
    parts = []
    for i, doc in enumerate(docs, 1):
        title = doc.metadata.get("title", "Financial Information")
        source = doc.metadata.get("source", "")
        parts.append(f"[{i}] {title} (Source: {source})\n{doc.page_content}")
    return "\n\n".join(parts)


def _extract_sources(docs) -> List[dict]:
    """Extract source metadata from retrieved documents."""
    seen = set()
    sources = []
    for doc in docs:
        title = doc.metadata.get("title", "")
        if title not in seen:
            seen.add(title)
            sources.append(
                {
                    "title": title,
                    "category": doc.metadata.get("category", ""),
                    "source": doc.metadata.get("source", ""),
                }
            )
    return sources


def _condense_question(
    question: str,
    history: List[ChatMessage],
) -> str:
    """
    If there's conversation history, rewrite the follow-up question as a
    standalone question so the retriever gets better results.
    """
    if not history:
        return question
    try:
        llm = get_granite_llm()
        chain = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
        result = chain.invoke(
            {
                "chat_history": _format_chat_history(history),
                "question": question,
            }
        )
        condensed = result.get("text", question).strip()
        logger.debug("Condensed question: %s", condensed)
        return condensed if condensed else question
    except Exception as exc:
        logger.warning("Question condensation failed: %s — using original.", exc)
        return question


def answer(
    query: str,
    history: Optional[List[ChatMessage]] = None,
    category_filter: Optional[str] = None,
    user_lang: Optional[str] = None,
) -> ChatResponse:
    """
    Main RAG entrypoint.

    Args:
        query:           The user's question (any supported language).
        history:         Conversation history for multi-turn context.
        category_filter: Optional category to restrict retrieval scope.
        user_lang:       Override detected language (ISO 639-1 code).

    Returns:
        ChatResponse with the generated answer, sources, and metadata.
    """
    history = history or []

    # 1. Detect language and translate query to English
    english_query, detected_lang = translate_query_to_english(query)
    if user_lang:
        detected_lang = user_lang
    logger.info("Query language: %s | English: %s", detected_lang, english_query[:80])

    # 2. Condense follow-up question if history exists
    retrieval_query = _condense_question(english_query, history)

    # 3. Retrieve relevant context
    docs = similarity_search(
        query=retrieval_query,
        k=settings.top_k_results,
        filter_category=category_filter,
    )

    # 4. Build and run the RAG chain
    context = _format_context(docs)
    chat_history_str = _format_chat_history(history)

    llm = get_granite_llm()
    chain = LLMChain(llm=llm, prompt=RAG_PROMPT)
    try:
        result = chain.invoke(
            {
                "system_prompt": SYSTEM_PROMPT,
                "context": context,
                "chat_history": chat_history_str,
                "question": english_query,
            }
        )
        raw_answer = result.get("text", "").strip()
    except Exception as exc:
        logger.error("LLM chain failed: %s", exc, exc_info=True)
        raw_answer = (
            "I'm sorry, I encountered an error generating the response. "
            "Please try again or rephrase your question."
        )

    # 5. Translate answer back to the user's language
    final_answer = translate_response_to_user_lang(raw_answer, detected_lang)

    sources = _extract_sources(docs)
    logger.info("Response generated (%d chars, lang=%s)", len(final_answer), detected_lang)

    return ChatResponse(
        answer=final_answer,
        sources=sources,
        detected_language=detected_lang,
        english_query=english_query,
        category_hint=category_filter,
    )
