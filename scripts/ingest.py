"""
scripts/ingest.py
──────────────────
Standalone ingestion script — call this to rebuild the vector store.

Usage:
    python scripts/ingest.py
    python scripts/ingest.py --reset   # clears existing store before re-ingesting
"""

import argparse
import os
import sys

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.logging import logger


def ingest(reset: bool = False) -> None:
    if reset:
        logger.info("Resetting vector store …")
        from app.core.config import settings
        import shutil
        persist_dir = os.path.abspath(settings.vectorstore_dir)
        if os.path.exists(persist_dir):
            shutil.rmtree(persist_dir)
            logger.info("Vector store cleared: %s", persist_dir)

    logger.info("Starting knowledge base ingestion …")
    from app.rag.vectorstore import get_vectorstore
    store = get_vectorstore()
    count = store._collection.count()
    logger.info("Ingestion complete. %d chunks in vector store.", count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest financial documents into ChromaDB")
    parser.add_argument("--reset", action="store_true", help="Clear vector store before ingesting")
    args = parser.parse_args()
    ingest(reset=args.reset)
