"""Answer verification endpoints with AI-generated feedback."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Question
from app.db.session import get_db
from app.services.verifier import verify_answer, get_ai_feedback

router = APIRouter()


class VerifyAnswerRequest(BaseModel):
    question_id: int
    user_answer: str


@router.post("/verify-answer")
async def verify(request: VerifyAnswerRequest, db: AsyncSession = Depends(get_db)):
    """
    Verify answer and get AI feedback.
    :param request: Request with question_id and user_answer
    :param db: Async database session
    :return: Correctness and feedback
    """
    query = select(Question).filter(Question.id == request.question_id)
    result = await db.execute(query)
    q = result.scalar_one_or_none()

    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = verify_answer(request.user_answer, q.answer)

    ai_response = get_ai_feedback(q.question, request.user_answer, q.answer, is_correct)

    return {
        "is_correct": is_correct,
        "ai_response": ai_response,
    }
