"""
app/core/logging.py
────────────────────
Structured JSON logging setup used across the application.
"""

import logging
import sys

from app.core.config import settings


def setup_logging() -> logging.Logger:
    """Configure root logger and return the app logger."""
    log_format = (
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )
    logging.basicConfig(
        level=getattr(logging, settings .log_level , logging.INFO),
        format=log_format,
        stream=sys.stdout,
        force=True,
    )
    # Silence noisy third-party loggers
    for noisy in ("httpx", "httpcore", "urllib3", "chromadb.telemetry"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    return logging.getLogger("digital_finance_agent")


logger = setup_logging()
