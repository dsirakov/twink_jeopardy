"""FastAPI application for Jeopardy questions with AI-powered answer verification."""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.questions import router as question_router
from app.api.verify import router as verify_router
from app.db.session import Base, engine


async def init_db():
    """
    Initialize database tables.
    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan.
    :param app: FastAPI application
    :return: None
    """
    await init_db()
    yield


app = FastAPI(title="Jeopardy API", lifespan=lifespan)

app.include_router(question_router)
app.include_router(verify_router)
