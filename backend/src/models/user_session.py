from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from src.database.connection import Base

class UserSession(Base):
    __tablename__ = "user_sessions"

    session_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True)
    preferences = Column(Text, nullable=True)  # JSON as text
    bookmarks = Column(Text, nullable=True)  # JSON as text
    personalized_path = Column(Text, nullable=True)  # JSON as text
    last_accessed = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())