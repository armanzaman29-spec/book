from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from src.database.connection import get_db
from src.utils.logger import log_info, log_error
from src.services.rag_service import rag_service
from pydantic import BaseModel

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str] = None
    max_sources: int = 3

@router.post("/query")
async def query_content(request: QueryRequest, db: Session = Depends(get_db)):
    """
    General RAG query against textbook content
    """
    try:
        log_info(f"Processing query: {request.question[:50]}...")

        result = await rag_service.query(
            db=db,
            question=request.question,
            user_id=request.user_id,
            max_sources=request.max_sources
        )

        return result
    except Exception as e:
        log_error(f"Error during query processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))