from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from agent import RAGAgent
from retrieving import VectorDBRetriever
from config import settings
import structlog
import uuid
from tenacity import retry, stop_after_attempt, wait_exponential
from logging_config import get_logger_instance

router = APIRouter()
logger = get_logger_instance()

# Pydantic models
class Message(BaseModel):
    role: str = Field(..., description="Role of the message sender (user, assistant, system)")
    content: str = Field(..., description="Content of the message", min_length=1)

    @validator('role')
    def validate_role(cls, v):
        if v not in ['user', 'assistant', 'system']:
            raise ValueError('role must be one of: user, assistant, system')
        return v

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., max_items=50)
    query: str = Field(..., description="User's query", min_length=1, max_length=5000)
    max_tokens: Optional[int] = Field(default=settings.max_tokens, ge=1, le=4000)
    temperature: Optional[float] = Field(default=settings.temperature, ge=0.0, le=2.0)
    top_k: Optional[int] = Field(default=settings.retrieval_top_k, ge=1, le=20)

class ChatResponse(BaseModel):
    response: str
    context: List[str]
    sources: List[str]
    query: str
    model_used: str
    tokens_used: Optional[int] = None

class ErrorResponse(BaseModel):
    detail: str
    request_id: Optional[str] = None

# Initialize retriever and agent
retriever = VectorDBRetriever()
rag_agent = RAGAgent(retriever)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def _process_query_with_retry(query: str, messages: List[Message], max_tokens: int, temperature: float, top_k: int):
    """Internal function with retry logic for processing queries"""
    return await rag_agent.process_query(
        query=query,
        messages=[msg.dict() for msg in messages],
        max_tokens=max_tokens,
        temperature=temperature,
        top_k=top_k
    )

@router.post("/chat",
             response_model=ChatResponse,
             responses={
                 200: {"description": "Successful response"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
             })
async def chat_endpoint(request: ChatRequest, req: Request):
    """
    Main chat endpoint that processes user queries using RAG
    """
    request_id = req.headers.get("X-Request-ID", str(uuid.uuid4()))
    log = logger.bind(request_id=request_id)

    try:
        log.info("Processing chat request",
                 query_length=len(request.query),
                 message_count=len(request.messages),
                 max_tokens=request.max_tokens,
                 temperature=request.temperature)

        response, context, sources = await _process_query_with_retry(
            query=request.query,
            messages=request.messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_k=request.top_k
        )

        log.info("Chat request processed successfully")

        return ChatResponse(
            response=response,
            context=context,
            sources=sources,
            query=request.query,
            model_used=settings.openai_model
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        log.error("Error processing chat request", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )

class QueryRequest(BaseModel):
    question: str = Field(..., description="User's question", min_length=1, max_length=5000)
    user_id: Optional[str] = None
    max_sources: Optional[int] = Field(default=3, ge=1, le=10)

class SelectQueryRequest(BaseModel):
    selected_text: str = Field(..., description="Selected text", min_length=1)
    question: str = Field(..., description="User's question about selected text", min_length=1, max_length=5000)
    user_id: Optional[str] = None

class IngestRequest(BaseModel):
    chapter_ids: List[str] = Field(..., description="List of chapter IDs to ingest")
    force_reprocess: Optional[bool] = False

class EmbedRequest(BaseModel):
    chunk_ids: List[str] = Field(..., description="List of chunk IDs to embed")

@router.post("/query",
             responses={
                 200: {"description": "Successful response"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
             })
async def simple_query_endpoint(request: QueryRequest, req: Request):
    """
    Simple query endpoint that matches frontend's expected format
    """
    request_id = req.headers.get("X-Request-ID", str(uuid.uuid4()))
    log = logger.bind(request_id=request_id)

    try:
        log.info("Processing simple query request",
                 question_length=len(request.question),
                 user_id=request.user_id,
                 max_sources=request.max_sources)

        # Prepare messages for the RAG agent
        messages = [Message(role="user", content=request.question)]
        response, context, sources = await _process_query_with_retry(
            query=request.question,
            messages=messages,
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
            top_k=request.max_sources
        )

        log.info("Simple query request processed successfully")

        return {
            "answer": response,
            "sources": sources,
            "context": context
        }

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        log.error("Error processing simple query request", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )

@router.post("/select-query",
             response_model=ChatResponse,
             responses={
                 200: {"description": "Successful response"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
             })
async def select_query_endpoint(request: SelectQueryRequest, req: Request):
    """
    Endpoint for queries about selected text
    """
    request_id = req.headers.get("X-Request-ID", str(uuid.uuid4()))
    log = logger.bind(request_id=request_id)

    try:
        log.info("Processing select-query request",
                 selected_text_length=len(request.selected_text),
                 question_length=len(request.question))

        # Prepare messages for the RAG agent
        messages = [Message(role="user", content=request.selected_text)]
        response, context, sources = await _process_query_with_retry(
            query=request.question,
            messages=messages,
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
            top_k=settings.retrieval_top_k
        )

        log.info("Select-query request processed successfully")

        return ChatResponse(
            response=response,
            context=context,
            sources=sources,
            query=request.question,
            model_used=settings.openai_model
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        log.error("Error processing select-query request", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )

@router.post("/ingest",
             responses={
                 200: {"description": "Ingestion completed"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
             })
async def ingest_endpoint(request: IngestRequest, req: Request):
    """
    Endpoint for ingesting content (chapters) into the vector database
    """
    request_id = req.headers.get("X-Request-ID", str(uuid.uuid4()))
    log = logger.bind(request_id=request_id)

    try:
        log.info("Processing ingest request",
                 chapter_count=len(request.chapter_ids),
                 force_reprocess=request.force_reprocess)

        # In a real implementation, this would process the chapters and add them to the vector DB
        # For now, we'll just return a success message
        # TODO: Implement actual content ingestion logic

        result = {
            "message": f"Successfully processed {len(request.chapter_ids)} chapters",
            "chapter_ids": request.chapter_ids,
            "processed_count": len(request.chapter_ids),
            "force_reprocess": request.force_reprocess
        }

        log.info("Ingest request processed successfully")

        return result

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        log.error("Error processing ingest request", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing ingest: {str(e)}"
        )

@router.post("/embed",
             responses={
                 200: {"description": "Embedding completed"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
             })
async def embed_endpoint(request: EmbedRequest, req: Request):
    """
    Endpoint for generating embeddings for specific chunks
    """
    request_id = req.headers.get("X-Request-ID", str(uuid.uuid4()))
    log = logger.bind(request_id=request_id)

    try:
        log.info("Processing embed request",
                 chunk_count=len(request.chunk_ids))

        # In a real implementation, this would generate embeddings for the specified chunks
        # For now, we'll just return a success message
        # TODO: Implement actual embedding logic

        result = {
            "message": f"Successfully processed embeddings for {len(request.chunk_ids)} chunks",
            "chunk_ids": request.chunk_ids,
            "processed_count": len(request.chunk_ids)
        }

        log.info("Embed request processed successfully")

        return result

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        log.error("Error processing embed request", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing embed: {str(e)}"
        )


@router.post("/chat",
             response_model=ChatResponse,
             responses={
                 200: {"description": "Successful response"},
                 422: {"model": ErrorResponse, "description": "Validation error"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
             })
async def chat_endpoint(request: ChatRequest, req: Request):
    """
    Main chat endpoint that processes user queries using RAG
    """
    request_id = req.headers.get("X-Request-ID", str(uuid.uuid4()))
    log = logger.bind(request_id=request_id)

    try:
        log.info("Processing chat request",
                 query_length=len(request.query),
                 message_count=len(request.messages),
                 max_tokens=request.max_tokens,
                 temperature=request.temperature)

        response, context, sources = await _process_query_with_retry(
            query=request.query,
            messages=request.messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_k=request.top_k
        )

        log.info("Chat request processed successfully")

        return ChatResponse(
            response=response,
            context=context,
            sources=sources,
            query=request.query,
            model_used=settings.openai_model
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        log.error("Error processing chat request", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )

@router.get("/health")
async def api_health(req: Request):
    """
    Health check endpoint that verifies API components are working
    """
    request_id = req.headers.get("X-Request-ID", str(uuid.uuid4()))

    # Check if retriever is working
    try:
        # Simple check by attempting to access the vector store
        is_retriever_healthy = await retriever.health_check()
    except Exception as e:
        logger.error("Retriever health check failed", error=str(e), request_id=request_id)
        is_retriever_healthy = False

    # Check if agent is working
    try:
        # Simple check by ensuring the agent is initialized
        is_agent_healthy = rag_agent.is_healthy()
    except Exception as e:
        logger.error("Agent health check failed", error=str(e), request_id=request_id)
        is_agent_healthy = False

    status = "healthy" if (is_retriever_healthy and is_agent_healthy) else "unhealthy"

    return {
        "status": status,
        "retriever": "healthy" if is_retriever_healthy else "unhealthy",
        "agent": "healthy" if is_agent_healthy else "unhealthy",
        "version": settings.app_version,
        "request_id": request_id
    }