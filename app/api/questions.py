"""Jeopardy question retrieval endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import func
from app.db.models import Question
from app.db.session import get_db

router = APIRouter()


@router.get("/question")
async def get_random_question(
    round: str, value: int, db: AsyncSession = Depends(get_db)
):
    """
    Get random question by round and value.
    :param round: Jeopardy round
    :param value: Question value
    :param db: Async database session
    :return: Question data
    """
    query = (
        select(Question)
        .filter(Question.round == round, Question.value == value)
        .order_by(func.random())
        .limit(1)
    )

    result = await db.execute(query)
    q = result.scalar_one_or_none()

    if not q:
        raise HTTPException(status_code=404, detail="No question found")

    return {
        "question_id": q.id,
        "round": q.round,
        "category": q.category,
        "value": f"${q.value}",
        "question": q.question,
    }
