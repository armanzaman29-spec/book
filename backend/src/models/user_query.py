from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database.connection import Base

class UserQuery(Base):
    __tablename__ = "user_queries"

    query_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True)  # Optional for anonymous users
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    source_chunks = Column(Text, nullable=True)  # JSON as text
    query_type = Column(String, nullable=False)  # "general" or "selection"
    selected_text = Column(Text, nullable=True)  # For selection-only mode
    response_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())