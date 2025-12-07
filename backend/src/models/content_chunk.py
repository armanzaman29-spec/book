from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database.connection import Base

class ContentChunk(Base):
    __tablename__ = "content_chunks"

    chunk_id = Column(String, primary_key=True, index=True)
    chapter_id = Column(String, ForeignKey("chapters.chapter_id"), nullable=False)
    content = Column(Text, nullable=False)
    char_offset = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    source_url = Column(String, nullable=True)
    text_hash = Column(String, nullable=True)
    embedding_vector_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())