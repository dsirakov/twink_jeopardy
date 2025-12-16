"""Answer verification with multi-layered matching and AI feedback."""

import difflib
from app.services.llm_client import get_client


def normalize(text: str) -> str:
    return "".join(c.lower() for c in text if c.isalnum() or c.isspace())


def get_embedding(text: str) -> list:
    """Get semantic embedding from OpenAI."""
    client = get_client()
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def cosine_similarity(a: list, b: list) -> float:
    """Calculate cosine similarity between two embeddings."""
    import math

    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(x * x for x in b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0
    return dot_product / (magnitude_a * magnitude_b)


def verify_answer(
    user_answer: str, correct_answer: str, use_semantic: bool = True
) -> bool:
    """Verify if user answer matches correct answer.

    First tries fuzzy matching, then semantic similarity if enabled.
    """
    ua = normalize(user_answer)
    ca = normalize(correct_answer)

    # Exact match after normalization
    if ua == ca:
        return True

    # Fuzzy match (typo tolerance)
    fuzzy_ratio = difflib.SequenceMatcher(None, ua, ca).ratio()
    if fuzzy_ratio > 0.8:
        return True

    # Semantic similarity
    if use_semantic:
        try:
            user_emb = get_embedding(user_answer)
            correct_emb = get_embedding(correct_answer)
            similarity = cosine_similarity(user_emb, correct_emb)
            return similarity > 0.75
        except Exception as e:
            print(f"Error in semantic matching: {e}")
            return False

    return False


def get_ai_feedback(
    question: str, user_answer: str, correct_answer: str, is_correct: bool
) -> str:
    """Get AI-generated feedback on the user's answer."""
    client = get_client()
    prompt = f"""The user was asked: "{question}"
The correct answer is: "{correct_answer}"
The user answered: "{user_answer}"
Is correct: {is_correct}

Provide a brief, helpful response about their answer. If correct, acknowledge it and briefly explain why. If incorrect, gently correct them."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )
    return response.choices[0].message.content
