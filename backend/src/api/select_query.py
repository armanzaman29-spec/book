from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from src.database.connection import get_db
from src.utils.logger import log_info, log_error
from src.services.rag_service import rag_service
from pydantic import BaseModel

router = APIRouter()

class SelectQueryRequest(BaseModel):
    selected_text: str
    question: str
    user_id: Optional[str] = None

@router.post("/select-query")
async def select_query_content(request: SelectQueryRequest, db: Session = Depends(get_db)):
    """
    Selection-only mode query using provided text only
    """
    try:
        log_info(f"Processing selection-only query for text excerpt: {request.selected_text[:50]}...")

        result = await rag_service.selection_query(
            selected_text=request.selected_text,
            question=request.question,
            user_id=request.user_id
        )

        return result
    except Exception as e:
        log_error(f"Error during selection query processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))