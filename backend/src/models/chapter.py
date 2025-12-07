from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from src.database.connection import Base

class Chapter(Base):
    __tablename__ = "chapters"

    chapter_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    learning_objectives = Column(Text, nullable=True)  # JSON as text
    apa_references = Column(Text, nullable=True)  # JSON as text
    chunking_strategy = Column(String, nullable=True)
    embedding_ready = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())