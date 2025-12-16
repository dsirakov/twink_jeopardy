"""
Unit tests for question endpoints.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.db.session import Base, get_db
from app.db.models import Question
from datetime import date

pytestmark = pytest.mark.asyncio
pytest_plugins = ("pytest_asyncio",)

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./tests/test.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"timeout": 30})
AsyncTestingSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    """
    Override database dependency for testing.
    :return: Async test database session
    """
    async with AsyncTestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
async def setup_database():
    """
    Setup test database with sample data.
    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncTestingSessionLocal() as db:
        sample_question = Question(
            show_number=1,
            air_date=date(2023, 1, 1),
            round="Jeopardy!",
            category="Science",
            value=200,
            question="What is the chemical symbol for gold?",
            answer="Au",
        )
        db.add(sample_question)
        await db.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    """
    Create async test client.
    :return: AsyncClient instance
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def test_get_random_question_success(setup_database, client):
    """
    Test successful retrieval of random question.
    :return: None
    """
    response = await client.get("/question?round=Jeopardy!&value=200")
    assert response.status_code == 200
    data = response.json()
    assert "question_id" in data
    assert data["round"] == "Jeopardy!"
    assert data["category"] == "Science"
    assert data["value"] == "$200"
    assert "question" in data


async def test_get_random_question_not_found(setup_database, client):
    """
    Test question not found scenario.
    :return: None
    """
    response = await client.get("/question?round=Double Jeopardy!&value=500")
    assert response.status_code == 404
    assert response.json()["detail"] == "No question found"


async def test_get_random_question_missing_params(setup_database, client):
    """
    Test missing query parameters.
    :return: None
    """
    response = await client.get("/question")
    assert response.status_code == 422


async def test_get_random_question_invalid_value_type(setup_database, client):
    """
    Test invalid value parameter type.
    :return: None
    """
    response = await client.get("/question?round=Jeopardy!&value=invalid")
    assert response.status_code == 422
