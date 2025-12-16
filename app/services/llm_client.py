"""OpenAI client singleton for LLM operations."""

from openai import OpenAI
from app.config import settings

_client: OpenAI | None = None


def get_client() -> OpenAI:
    """
    Returns a singleton OpenAI client instance.

    This ensures:
      - Only one client is created
      - Easy to mock in tests
      - Centralized API key usage
    """
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment")
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client
