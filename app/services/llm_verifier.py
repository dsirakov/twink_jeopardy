"""LLM-based answer verification using GPT-4o-mini as a strict judge."""

from app.services.llm_client import get_client

SYSTEM_PROMPT = """
You are a strict trivia judge.
Given the original correct answer and a user's answer, 
decide if the user's answer should be considered correct.
- Allow minor spelling errors
- Allow synonymous phrasing
- Be strict about factual correctness
Respond ONLY with "YES" or "NO".
"""


def verify_with_llm(user_answer: str, correct_answer: str) -> bool:
    """
    Verify answer using LLM as judge.
    :param user_answer: User provided answer
    :param correct_answer: Correct answer
    :return: True if answer is correct
    """
    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Correct Answer: {correct_answer}\nUser Answer: {user_answer}",
            },
        ],
    )

    result = response.choices[0].message.content.strip().upper()
    return result == "YES"
