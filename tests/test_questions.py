"""
Unit tests for question endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base, get_db
from app.db.models import Question
from datetime import date


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    Override database dependency for testing.
    :return: Test database session
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """
    Setup test database with sample data.
    :return: None
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

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
    db.commit()

    yield

    db.close()
    Base.metadata.drop_all(bind=engine)


def test_get_random_question_success():
    """
    Test successful retrieval of random question.
    :return: None
    """
    response = client.get("/question?round=Jeopardy!&value=200")
    assert response.status_code == 200
    data = response.json()
    assert "question_id" in data
    assert data["round"] == "Jeopardy!"
    assert data["category"] == "Science"
    assert data["value"] == "$200"
    assert "question" in data


def test_get_random_question_not_found():
    """
    Test question not found scenario.
    :return: None
    """
    response = client.get("/question?round=Double Jeopardy!&value=500")
    assert response.status_code == 404
    assert response.json()["detail"] == "No question found"


def test_get_random_question_missing_params():
    """
    Test missing query parameters.
    :return: None
    """
    response = client.get("/question")
    assert response.status_code == 422


def test_get_random_question_invalid_value_type():
    """
    Test invalid value parameter type.
    :return: None
    """
    response = client.get("/question?round=Jeopardy!&value=invalid")
    assert response.status_code == 422
