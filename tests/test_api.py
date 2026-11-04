"""
tests/test_api.py
──────────────────
Integration tests for the FastAPI endpoints.
Run with: pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_schema(self):
        data = client.get("/health").json()
        assert "status" in data
        assert "vectorstore_loaded" in data
        assert "llm_model" in data
        assert "supported_languages" in data
        assert isinstance(data["supported_languages"], list)
        assert "en" in data["supported_languages"]


class TestTopicsEndpoint:
    def test_topics_returns_list(self):
        response = client.get("/topics")
        assert response.status_code == 200
        data = response.json()
        assert "topics" in data
        assert isinstance(data["topics"], list)
        assert len(data["topics"]) > 0

    def test_topic_has_required_fields(self):
        topics = client.get("/topics").json()["topics"]
        for topic in topics:
            assert "id" in topic
            assert "label" in topic
            assert "sample_query" in topic


class TestLanguagesEndpoint:
    def test_languages_returns_200(self):
        response = client.get("/languages")
        assert response.status_code == 200

    def test_languages_contains_hindi(self):
        data = client.get("/languages").json()
        codes = [l["code"] for l in data["supported_languages"]]
        assert "hi" in codes
        assert "en" in codes


class TestChatEndpoint:
    def test_chat_basic_english_question(self):
        response = client.post(
            "/chat",
            json={"message": "How do I send money via UPI?", "history": []},
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert len(data["answer"]) > 20
        assert "detected_language" in data
        assert "sources" in data

    def test_chat_with_category_filter(self):
        response = client.post(
            "/chat",
            json={
                "message": "What is a safe interest rate for a personal loan?",
                "category": "interest_rates",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data

    def test_chat_with_conversation_history(self):
        history = [
            {"role": "user", "content": "What is UPI?"},
            {"role": "assistant", "content": "UPI is a real-time payment system by NPCI."},
        ]
        response = client.post(
            "/chat",
            json={
                "message": "How do I get a UPI ID?",
                "history": history,
            },
        )
        assert response.status_code == 200
        assert len(response.json()["answer"]) > 10

    def test_chat_scam_prevention_query(self):
        response = client.post(
            "/chat",
            json={"message": "What are common online payment scams?"},
        )
        assert response.status_code == 200

    def test_chat_empty_message_returns_422(self):
        response = client.post("/chat", json={"message": ""})
        assert response.status_code == 422

    def test_chat_message_too_long_returns_422(self):
        response = client.post("/chat", json={"message": "x" * 1001})
        assert response.status_code == 422

    def test_chat_invalid_language_code_returns_422(self):
        response = client.post(
            "/chat",
            json={"message": "Hello", "language": "xyz123"},
        )
        assert response.status_code == 422


class TestFrontend:
    def test_frontend_serves_html(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "FinSaathi" in response.text
