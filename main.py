"""
main.py
────────
FastAPI application entry point.

Startup sequence:
  1. Load .env config
  2. Set up logging
  3. Pre-load vector store (with ingestion if needed)
  4. Pre-load embedding model
  5. Register routes + middleware
  6. Serve
"""

from __future__ import annotations

import logging
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import settings
from app.core.logging import logger

# ── Create the FastAPI app ────────────────────────────────────────────────────
app = FastAPI(
    title="Digital Financial Literacy AI Agent",
    description=(
        "An AI agent powered by IBM Granite (watsonx.ai) and RAG to help users "
        "understand UPI, avoid scams, manage budgets, and navigate personal finance. "
        "Supports multilingual input (EN, HI, TA, TE, BN, MR, GU, KN, ML, PA, UR)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Digital Finance Agent",
        "url": "https://github.com/your-org/digital-financial-ai-agent",
    },
    license_info={"name": "MIT"},
)

# ── CORS Middleware ───────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ── Request logging middleware ────────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s → %d (%.1fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


# ── Global exception handler ─────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception on %s: %s", request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "code": "INTERNAL_ERROR"},
    )


# ── Startup event: pre-warm models ───────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("  Digital Financial Literacy AI Agent  v1.0.0")
    logger.info("  Powered by IBM Granite (watsonx.ai)")
    logger.info("=" * 60)
    logger.info("Environment: %s", settings.app_env)
    logger.info("Granite model: %s", settings.ibm_granite_model_id)
    logger.info("Supported languages: %s", settings.supported_languages)

    # Pre-load vector store (triggers ingestion if empty)
    logger.info("Pre-loading vector store …")
    try:
        from app.rag.vectorstore import get_vectorstore
        store = get_vectorstore()
        count = store._collection.count()
        logger.info("Vector store ready: %d chunks.", count)
    except Exception as exc:
        logger.error("Vector store initialization failed: %s", exc, exc_info=True)

    # Pre-load embedding model
    logger.info("Pre-loading embedding model …")
    try:
        from app.rag.embeddings import get_embedding_model
        get_embedding_model()
        logger.info("Embedding model loaded.")
    except Exception as exc:
        logger.error("Embedding model initialization failed: %s", exc, exc_info=True)

    logger.info("Startup complete. Server ready at http://%s:%d", settings.app_host, settings.app_port)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Digital Financial Literacy AI Agent.")


# ── Static files (CSS, JS, images) ───────────────────────────────────────────
import os
static_dir = os.path.join(os.path.dirname(__file__), "frontend", "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ── Register API routes ───────────────────────────────────────────────────────
app.include_router(router)


# ── Direct run ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "development",
        log_level=settings.log_level.lower(),
    )
