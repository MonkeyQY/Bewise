from sqlalchemy import Column, String, Text, Integer, DateTime, func, JSON, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database

from app.Task1.database import metadata, engine

Base = declarative_base(metadata=metadata)


class QuestionDB(Base):
    __tablename__ = "questions"
    id = Column(BigInteger, primary_key=True, index=True)
    answer = Column(String)
    question = Column(Text)
    value = Column(Integer)
    airdate = Column(String)
    created_at = Column(DateTime, index=True, default=func.now())
    updated_at = Column(String)
    category_id = Column(Integer, index=True)
    game_id = Column(Integer)
    invalid_count = Column(Integer)
    category = Column(JSON)


if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
