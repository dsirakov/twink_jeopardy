from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db.session import SessionLocal
from app.db.models import Question

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/question")
def get_random_question(round: str, value: int, db: Session = Depends(get_db)):
    q = (
        db.query(Question)
        .filter(Question.round == round, Question.value == value)
        .order_by(func.random())
        .first()
    )

    if not q:
        raise HTTPException(status_code=404, detail="No question found")

    return {
        "question_id": q.id,
        "round": q.round,
        "category": q.category,
        "value": f"${q.value}",
        "question": q.question,
    }
