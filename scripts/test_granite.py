"""
scripts/test_granite.py
────────────────────────
Quick sanity-check script to verify IBM Granite connectivity.

Usage:
    python scripts/test_granite.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.logging import logger
from app.agent.granite_llm import get_granite_llm


def main():
    logger.info("Testing IBM Granite LLM connectivity …")
    llm = get_granite_llm()
    test_prompt = (
        "You are a helpful financial advisor. "
        "In one sentence, what is UPI?"
    )
    logger.info("Sending test prompt to Granite …")
    response = llm._call(test_prompt)
    print("\n" + "=" * 60)
    print("GRANITE RESPONSE:")
    print(response)
    print("=" * 60 + "\n")
    logger.info("Test complete.")


if __name__ == "__main__":
    main()
