from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.models import Question
from app.db.session import get_db
from app.services.verifier import verify_answer, get_ai_feedback

router = APIRouter()


class VerifyAnswerRequest(BaseModel):
    question_id: int
    user_answer: str


@router.post("/verify-answer")
def verify(request: VerifyAnswerRequest, db: Session = Depends(get_db)):
    """Verify user answer and provide AI feedback."""
    q = db.query(Question).filter(Question.id == request.question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = verify_answer(request.user_answer, q.answer)

    # Get AI feedback
    ai_response = get_ai_feedback(q.question, request.user_answer, q.answer, is_correct)

    return {
        "is_correct": is_correct,
        "ai_response": ai_response,
    }
