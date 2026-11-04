"""
tests/test_rag.py
──────────────────
Unit tests for the RAG pipeline components.
"""

import pytest
from app.rag.knowledge_base import FINANCIAL_DOCUMENTS
from app.rag.vectorstore import _build_documents, similarity_search


class TestKnowledgeBase:
    def test_knowledge_base_not_empty(self):
        assert len(FINANCIAL_DOCUMENTS) > 0

    def test_all_documents_have_required_fields(self):
        required = {"id", "title", "category", "language", "source", "content"}
        for doc in FINANCIAL_DOCUMENTS:
            missing = required - set(doc.keys())
            assert not missing, f"Document {doc.get('id')} missing fields: {missing}"

    def test_all_documents_have_content(self):
        for doc in FINANCIAL_DOCUMENTS:
            assert len(doc["content"].strip()) > 50, f"Document {doc['id']} has too little content"

    def test_categories_are_valid(self):
        valid_categories = {
            "upi", "scam_prevention", "interest_rates",
            "budgeting", "personal_finance", "government_schemes",
        }
        for doc in FINANCIAL_DOCUMENTS:
            assert doc["category"] in valid_categories, \
                f"Document {doc['id']} has invalid category: {doc['category']}"


class TestDocumentBuilding:
    def test_build_documents_returns_chunks(self):
        docs = _build_documents()
        assert len(docs) > len(FINANCIAL_DOCUMENTS)  # should be chunked

    def test_chunks_have_metadata(self):
        docs = _build_documents()
        for doc in docs:
            assert doc.metadata.get("title")
            assert doc.metadata.get("category")


class TestVectorStore:
    def test_similarity_search_returns_results(self):
        results = similarity_search("How to send money via UPI?", k=3)
        assert len(results) > 0
        assert len(results) <= 3

    def test_similarity_search_upi_query(self):
        results = similarity_search("UPI payment steps", k=3)
        categories = [r.metadata.get("category") for r in results]
        assert "upi" in categories

    def test_similarity_search_scam_query(self):
        results = similarity_search("online fraud and scams", k=3)
        assert len(results) > 0

    def test_similarity_search_with_category_filter(self):
        results = similarity_search(
            "interest rate for home loan",
            k=5,
            filter_category="interest_rates",
        )
        for r in results:
            assert r.metadata.get("category") == "interest_rates"
