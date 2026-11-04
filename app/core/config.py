"""
app/core/config.py
──────────────────
Central settings loaded from the .env file via pydantic-settings.
All other modules import `settings` from here.
"""

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── IBM watsonx.ai ──────────────────────────────────────────────
    ibm_watsonx_api_key: str = Field(..., description="IBM Cloud API key")
    ibm_watsonx_url: str = Field(
        "https://us-south.ml.cloud.ibm.com", description="watsonx.ai endpoint"
    )
    ibm_watsonx_project_id: str = Field(..., description="watsonx.ai project ID")
    ibm_granite_model_id: str = Field(
        "ibm/granite-13b-instruct-v2", description="Granite model ID"
    )

    # ── IBM Watson Language Translator ──────────────────────────────
    ibm_translator_api_key: str = Field("", description="Translator API key (optional)")
    ibm_translator_url: str = Field("", description="Translator service URL (optional)")

    # ── Application ─────────────────────────────────────────────────
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_env: str = "development"
    secret_key: str = "changeme"
    log_level: str = "INFO"

    # ── RAG / Vector Store ──────────────────────────────────────────
    vectorstore_dir: str = "./data/vectorstore"
    documents_dir: str = "./data/documents"
    chunk_size: int = 512
    chunk_overlap: int = 64
    top_k_results: int = 5

    # ── LLM Generation ──────────────────────────────────────────────
    llm_max_new_tokens: int = 512
    llm_temperature: float = 0.3
    llm_top_p: float = 0.9
    llm_repetition_penalty: float = 1.1

    # ── Embeddings ──────────────────────────────────────────────────
    embedding_model: str = (
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # ── Language support ────────────────────────────────────────────
    supported_languages: str = "en,hi,ta,te,bn,mr,gu,kn,ml,pa,ur"

    @property
    def supported_languages_list(self) -> List[str]:
        return [lang.strip() for lang in self.supported_languages.split(",")]

    # ── Rate limiting ───────────────────────────────────────────────
    rate_limit_requests: int = 20
    rate_limit_window_seconds: int = 60

    # ── CORS ────────────────────────────────────────────────────────
    cors_origins: str = "*"

    @property
    def cors_origins_list(self) -> List[str]:
        if self.cors_origins == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",")]

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper = v.upper()
        if upper not in allowed:
            raise ValueError(f"log_level must be one of {allowed}")
        return upper


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
