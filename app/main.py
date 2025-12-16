from fastapi import FastAPI
from app.api.questions import router as question_router
from app.db.session import Base, engine

Base.metadata.create_all(engine)

app = FastAPI(title="Jeopardy API")

app.include_router(question_router)
