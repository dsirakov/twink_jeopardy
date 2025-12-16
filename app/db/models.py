"""SQLAlchemy ORM models for Jeopardy questions."""

from sqlalchemy import Column, Integer, String, Date
from app.db.session import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    show_number = Column(Integer)
    air_date = Column(Date)
    round = Column(String)
    category = Column(String)
    value = Column(Integer)
    question = Column(String)
    answer = Column(String)
