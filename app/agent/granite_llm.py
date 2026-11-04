"""
app/agent/granite_llm.py
─────────────────────────
IBM Granite LLM wrapper via watsonx.ai (IBM Cloud Lite).

Uses the ibm-watsonx-ai SDK to call IBM Granite models.
Falls back to a mock LLM when IBM_WATSONX_API_KEY is set to the
placeholder value 'your_ibm_cloud_api_key_here', allowing local dev
without real credentials.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any, Dict, Iterator, List, Optional

from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun

from app.core.config import settings

logger = logging.getLogger("digital_finance_agent.granite_llm")

_PLACEHOLDER_KEY = "your_ibm_cloud_api_key_here"


class GraniteLLM(LLM):
    """
    LangChain-compatible wrapper around IBM watsonx.ai Granite models.

    Attributes:
        model_id:    IBM Granite model identifier.
        project_id:  watsonx.ai project ID.
        api_key:     IBM Cloud API key.
        url:         watsonx.ai service URL.
        params:      TextGenParameters dict passed to the API.
    """

    model_id: str = settings.ibm_granite_model_id
    project_id: str = settings.ibm_watsonx_project_id
    api_key: str = settings.ibm_watsonx_api_key
    url: str = settings.ibm_watsonx_url
    params: Dict[str, Any] = {
        "max_new_tokens": settings.llm_max_new_tokens,
        "temperature": settings.llm_temperature,
        "top_p": settings.llm_top_p,
        "repetition_penalty": settings.llm_repetition_penalty,
        "stop_sequences": ["Human:", "User:", "\n\nQuestion:"],
    }

    @property
    def _llm_type(self) -> str:
        return "ibm_granite_watsonx"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        # Dev fallback — placeholder key
        if self.api_key == _PLACEHOLDER_KEY:
            logger.warning(
                "IBM_WATSONX_API_KEY is a placeholder. Using mock response for development."
            )
            return self._mock_response(prompt)

        try:
            from ibm_watsonx_ai import Credentials
            from ibm_watsonx_ai.foundation_models import ModelInference
            from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

            credentials = Credentials(url=self.url, api_key=self.api_key)
            gen_params = {
                GenParams.MAX_NEW_TOKENS: self.params["max_new_tokens"],
                GenParams.TEMPERATURE: self.params["temperature"],
                GenParams.TOP_P: self.params["top_p"],
                GenParams.REPETITION_PENALTY: self.params["repetition_penalty"],
            }
            if stop:
                gen_params[GenParams.STOP_SEQUENCES] = stop
            elif self.params.get("stop_sequences"):
                gen_params[GenParams.STOP_SEQUENCES] = self.params["stop_sequences"]

            model = ModelInference(
                model_id=self.model_id,
                credentials=credentials,
                project_id=self.project_id,
                params=gen_params,
            )
            response = model.generate_text(prompt=prompt)
            logger.debug("Granite response (%d chars)", len(response))
            return response.strip()

        except ImportError:
            logger.error(
                "ibm-watsonx-ai package not installed. Run: pip install ibm-watsonx-ai"
            )
            return "I'm sorry, the IBM watsonx.ai SDK is not installed. Please install it with: pip install ibm-watsonx-ai"
        except Exception as exc:
            logger.error("Granite API call failed: %s", exc, exc_info=True)
            return f"I encountered an error connecting to IBM watsonx.ai: {exc}. Please check your API credentials."

    def _mock_response(self, prompt: str) -> str:
        """Return a structured mock response for development/testing."""
        prompt_lower = prompt.lower()
        if "upi" in prompt_lower:
            return (
                "UPI (Unified Payments Interface) is a real-time payment system by NPCI. "
                "To send money: open your UPI app, choose 'Send Money', enter the recipient's "
                "UPI ID or scan their QR code, enter the amount, and confirm with your UPI PIN. "
                "Remember: you ONLY enter your PIN to SEND money, never to receive it."
            )
        if "scam" in prompt_lower or "fraud" in prompt_lower:
            return (
                "Protect yourself from online scams: never share your OTP, UPI PIN, or CVV "
                "with anyone. Reject unknown UPI collect requests. A QR code can never give "
                "you money — that's always a scam. Report fraud to the National Cyber Crime "
                "Helpline at 1930 or at cybercrime.gov.in."
            )
        if "interest" in prompt_lower or "loan" in prompt_lower:
            return (
                "Safe loan interest rates in India: Home loans typically range 8.5–10.5% per annum, "
                "personal loans 10–24% PA. Be cautious of any lender charging more than 26% PA — "
                "this may be predatory. Always verify the lender is RBI-registered at rbi.org.in."
            )
        if "budget" in prompt_lower or "saving" in prompt_lower:
            return (
                "A simple budgeting rule is the 50/30/20 approach: 50% on needs, 30% on wants, "
                "and 20% on savings and investments. Start by tracking your expenses for one month "
                "to understand where your money goes, then set a realistic savings target."
            )
        return (
            "I'm your Digital Financial Literacy Assistant. I can help you with UPI payments, "
            "avoiding online scams, understanding interest rates, budgeting, and personal finance. "
            "What would you like to know?"
        )

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"model_id": self.model_id, "project_id": self.project_id}


@lru_cache(maxsize=1)
def get_granite_llm() -> GraniteLLM:
    """Return a cached singleton GraniteLLM instance."""
    logger.info("Initialising IBM Granite LLM: %s", settings.ibm_granite_model_id)
    return GraniteLLM()
