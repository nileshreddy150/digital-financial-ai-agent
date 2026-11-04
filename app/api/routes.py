"""
app/api/routes.py
──────────────────
FastAPI route definitions for the Digital Financial Literacy Agent.

Endpoints:
  GET  /               → Serve the frontend HTML
  GET  /health         → Service health check
  POST /chat           → Main RAG chat endpoint
  GET  /topics         → Quick-access financial topics
  GET  /languages      → Supported languages list
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.agent.rag_chain import answer, ChatMessage
from app.api.models import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    QuickTopicResponse,
    ErrorResponse,
)
from app.core.config import settings
from app.i18n.translator import LANGUAGE_NAMES
from app.rag.vectorstore import get_vectorstore

logger = logging.getLogger("digital_finance_agent.routes")
router = APIRouter()

_START_TIME = time.time()
APP_VERSION = "1.0.0"

# Quick-access topics shown in the UI
QUICK_TOPICS = [
    {"id": "upi", "label": "💳 UPI & Digital Payments", "sample_query": "How do I send money via UPI?"},
    {"id": "scam_prevention", "label": "🛡️ Avoid Online Scams", "sample_query": "What are common UPI scams and how to avoid them?"},
    {"id": "interest_rates", "label": "📊 Interest Rates", "sample_query": "What is a safe interest rate for a loan?"},
    {"id": "budgeting", "label": "💰 Budgeting", "sample_query": "How do I create a monthly budget?"},
    {"id": "personal_finance", "label": "📈 Investments", "sample_query": "What are good investment options for beginners?"},
    {"id": "personal_finance", "label": "💳 Credit Score", "sample_query": "How can I improve my CIBIL credit score?"},
    {"id": "government_schemes", "label": "🏛️ Govt Schemes", "sample_query": "What are government financial schemes I can benefit from?"},
    {"id": "personal_finance", "label": "🛡️ Insurance", "sample_query": "What insurance should every person have?"},
]


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_frontend():
    """Serve the main chat frontend."""
    frontend_path = Path(__file__).parent.parent.parent / "frontend" / "index.html"
    if frontend_path.exists():
        return HTMLResponse(content=frontend_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h2>Frontend not found. Please place index.html in /frontend/</h2>", status_code=404)


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Return service health status."""
    try:
        store = get_vectorstore()
        vs_loaded = store._collection.count() > 0
    except Exception:
        vs_loaded = False

    return HealthResponse(
        status="healthy",
        version=APP_VERSION,
        vectorstore_loaded=vs_loaded,
        llm_model=settings.ibm_granite_model_id,
        supported_languages=settings.supported_languages_list,
    )


@router.post(
    "/chat",
    response_model=ChatResponse,
    tags=["Chat"],
    summary="Ask a financial literacy question",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        503: {"model": ErrorResponse, "description": "LLM service unavailable"},
    },
)
async def chat(request: ChatRequest):
    """
    Main RAG endpoint. Accepts a user message and optional conversation history.
    Supports multilingual input — the agent detects the language automatically.
    """
    logger.info("Chat request | lang=%s | msg='%s'", request.language, request.message[:80])

    # Convert schema messages to internal ChatMessage objects
    history = [
        ChatMessage(role=m.role, content=m.content) for m in request.history
    ]

    response = answer(
        query=request.message,
        history=history,
        category_filter=request.category,
        user_lang=request.language,
    )

    return ChatResponse(
        answer=response.answer,
        sources=[
            {"title": s["title"], "category": s["category"], "source": s["source"]}
            for s in response.sources
        ],
        detected_language=response.detected_language,
        english_query=response.english_query,
    )


@router.get("/topics", response_model=QuickTopicResponse, tags=["Discovery"])
async def get_topics():
    """Return quick-access financial topics with sample queries."""
    return QuickTopicResponse(topics=QUICK_TOPICS)


@router.get("/languages", tags=["Discovery"])
async def get_languages():
    """Return all supported languages."""
    supported = settings.supported_languages_list
    return {
        "supported_languages": [
            {"code": code, "name": LANGUAGE_NAMES.get(code, code)}
            for code in supported
        ]
    }
