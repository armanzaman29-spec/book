from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from src.database.connection import get_db
from src.utils.logger import log_info, log_error
from src.services.rag_service import rag_service
from pydantic import BaseModel

router = APIRouter()

class EmbedRequest(BaseModel):
    chunk_ids: List[str]

@router.post("/embed")
async def embed_content(request: EmbedRequest, db: Session = Depends(get_db)):
    """
    Generate embeddings for content chunks
    """
    try:
        log_info(f"Starting embedding generation for {len(request.chunk_ids)} chunks")

        # In a real implementation, we would generate embeddings for the specified chunks
        # For now, we'll return a placeholder response
        # This would typically involve:
        # 1. Fetching the content chunks from the database
        # 2. Generating embeddings using the Gemini API
        # 3. Storing embeddings in the vector database
        # 4. Updating the database with embedding references

        result = await rag_service.generate_embeddings(db, request.chunk_ids)

        return result
    except Exception as e:
        log_error(f"Error during embedding generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))