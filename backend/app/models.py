from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    clerk_user_id = Column(String, nullable=False, index=True)
    filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    created_at = Column(DateTime, default=_utcnow)

    chunks = relationship(
        "Chunk", back_populates="document", cascade="all, delete-orphan"
    )


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(
        Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    content = Column(Text, nullable=False)
    embedding = Column(Vector(768))
    created_at = Column(DateTime, default=_utcnow)

    document = relationship("Document", back_populates="chunks")
