"""OpenAI client singleton for LLM operations."""

from openai import OpenAI
from app.config import settings

_client: OpenAI | None = None


def get_client() -> OpenAI:
    """
    Get singleton OpenAI client.
    :return: OpenAI client instance
    """
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment")
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client
