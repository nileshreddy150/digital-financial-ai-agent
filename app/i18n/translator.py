"""
app/i18n/translator.py
───────────────────────
Multilingual support layer.

Priority:
  1. IBM Watson Language Translator (if API key is configured)
  2. Deep-Translator / LibreTranslate (free fallback, no key needed)
  3. Pass-through (return text unchanged) if translation fails
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Optional

from app.core.config import settings

logger = logging.getLogger("digital_finance_agent.translator")

# ISO 639-1 → human-readable display name for UI
LANGUAGE_NAMES: dict[str, str] = {
    "en": "English",
    "hi": "Hindi (हिन्दी)",
    "ta": "Tamil (தமிழ்)",
    "te": "Telugu (తెలుగు)",
    "bn": "Bengali (বাংলা)",
    "mr": "Marathi (मराठी)",
    "gu": "Gujarati (ગુજરાતી)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "ml": "Malayalam (മലയാളം)",
    "pa": "Punjabi (ਪੰਜਾਬੀ)",
    "ur": "Urdu (اردو)",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ar": "Arabic",
    "zh": "Chinese (Simplified)",
}


def _translate_via_ibm(text: str, source_lang: str, target_lang: str) -> Optional[str]:
    """Attempt translation using IBM Watson Language Translator."""
    if not settings.ibm_translator_api_key or not settings.ibm_translator_url:
        return None
    try:
        from ibm_watson import LanguageTranslatorV3
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

        authenticator = IAMAuthenticator(settings.ibm_translator_api_key)
        lt = LanguageTranslatorV3(version="2018-05-01", authenticator=authenticator)
        lt.set_service_url(settings.ibm_translator_url)

        model_id = f"{source_lang}-{target_lang}"
        result = lt.translate(text=[text], model_id=model_id).get_result()
        translated = result["translations"][0]["translation"]
        logger.debug("IBM Translator: %s → %s (%d chars)", source_lang, target_lang, len(translated))
        return translated
    except Exception as exc:
        logger.warning("IBM Translator failed (%s) — falling back.", exc)
        return None


def _translate_via_deep_translator(
    text: str, source_lang: str, target_lang: str
) -> Optional[str]:
    """Attempt translation using deep-translator (Google backend, free)."""
    try:
        from deep_translator import GoogleTranslator

        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        logger.debug("deep-translator: %s → %s", source_lang, target_lang)
        return translated
    except Exception as exc:
        logger.warning("deep-translator failed (%s).", exc)
        return None


def detect_language(text: str) -> str:
    """
    Detect the language of the input text.
    Returns ISO 639-1 code (default 'en' on failure).
    """
    try:
        from langdetect import detect

        lang = detect(text)
        return lang if lang in settings.supported_languages_list else "en"
    except Exception:
        return "en"


def translate(
    text: str,
    target_lang: str,
    source_lang: str = "en",
) -> str:
    """
    Translate `text` from `source_lang` to `target_lang`.
    Returns the original text if translation is not needed or fails.
    """
    if source_lang == target_lang or not text.strip():
        return text

    # Try IBM Watson first
    result = _translate_via_ibm(text, source_lang, target_lang)
    if result:
        return result

    # Try deep-translator fallback
    result = _translate_via_deep_translator(text, source_lang, target_lang)
    if result:
        return result

    # Pass-through: return unchanged
    logger.warning(
        "All translation backends failed for %s → %s. Returning original.", source_lang, target_lang
    )
    return text


def translate_query_to_english(query: str) -> tuple[str, str]:
    """
    Detect the language of `query` and translate it to English if needed.

    Returns:
        (english_query, detected_lang)
    """
    detected = detect_language(query)
    if detected == "en":
        return query, "en"
    english = translate(query, target_lang="en", source_lang=detected)
    return english, detected


def translate_response_to_user_lang(response: str, user_lang: str) -> str:
    """Translate an English response into the user's language."""
    if user_lang == "en":
        return response
    return translate(response, target_lang=user_lang, source_lang="en")
