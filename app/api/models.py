"""
app/api/models.py
──────────────────
Pydantic request/response schemas for the FastAPI endpoints.
"""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class ChatMessageSchema(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$", description="Message role")
    content: str = Field(..., min_length=1, max_length=4000, description="Message text")

    model_config = {"json_schema_extra": {"example": {"role": "user", "content": "How do I send money via UPI?"}}}


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The user's question or message",
    )
    history: List[ChatMessageSchema] = Field(
        default_factory=list,
        max_length=20,
        description="Prior conversation turns (up to 20 messages)",
    )
    language: Optional[str] = Field(
        None,
        pattern="^[a-z]{2}$",
        description="Override detected language (ISO 639-1, e.g. 'hi', 'ta')",
    )
    category: Optional[str] = Field(
        None,
        description="Restrict retrieval to a category: upi, scam_prevention, interest_rates, budgeting, personal_finance, government_schemes",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "What is a safe interest rate for a personal loan?",
                "history": [],
                "language": None,
                "category": "interest_rates",
            }
        }
    }


class SourceSchema(BaseModel):
    title: str
    category: str
    source: str


class ChatResponse(BaseModel):
    answer: str = Field(..., description="The generated answer")
    sources: List[SourceSchema] = Field(
        default_factory=list, description="Knowledge sources used"
    )
    detected_language: str = Field(..., description="ISO 639-1 code of detected input language")
    english_query: str = Field(..., description="Query translated to English for retrieval")

    model_config = {
        "json_schema_extra": {
            "example": {
                "answer": "For a personal loan, safe interest rates range from 10% to 24% per annum...",
                "sources": [{"title": "Understanding Loan Interest Rates", "category": "interest_rates", "source": "RBI / NHB"}],
                "detected_language": "en",
                "english_query": "What is a safe interest rate for a personal loan?",
            }
        }
    }


class HealthResponse(BaseModel):
    status: str
    version: str
    vectorstore_loaded: bool
    llm_model: str
    supported_languages: List[str]


class QuickTopicResponse(BaseModel):
    topics: List[dict]


class ErrorResponse(BaseModel):
    detail: str
    code: str
