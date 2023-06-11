import uuid

from sqlalchemy import Column, String, LargeBinary, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database

from app.Task2.database import metadata, engine

Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "user"
    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        index=True,
        primary_key=True,
        unique=True,
    )
    name = Column(String, nullable=False)
    api_token = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True)
    created_at = Column(DateTime, index=True, default=func.now())


class Audio(Base):
    __tablename__ = "audio"
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, primary_key=True)
    user_id = Column(ForeignKey("user.id"))
    audio = Column(LargeBinary)


if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
