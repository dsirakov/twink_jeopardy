"""FastAPI application for Jeopardy questions with AI-powered answer verification."""

from fastapi import FastAPI
from app.api.questions import router as question_router
from app.api.verify import router as verify_router
from app.db.session import Base, engine

Base.metadata.create_all(engine)

app = FastAPI(title="Jeopardy API")

app.include_router(question_router)
app.include_router(verify_router)
