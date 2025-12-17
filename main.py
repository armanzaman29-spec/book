import os
import sys
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

# Load environment variables first before importing other modules
from dotenv import load_dotenv
load_dotenv()

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
from config import settings
from logging_config import get_logger_instance

# Import after settings are loaded
from api import router

import uvicorn

logger = get_logger_instance()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager for startup and shutdown events
    """
    # Startup
    logger.info("Starting RAG Chatbot API", version=settings.app_version)

    try:
        # Validate configuration
        settings.validate_required_keys()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error("Configuration validation failed", error=str(e))
        sys.exit(1)

    yield

    # Shutdown
    logger.info("Shutting down RAG Chatbot API")

app = FastAPI(
    title=settings.app_name,
    description="A Production-Ready Retrieval-Augmented Generation chatbot using OpenAI agents",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Add Prometheus metrics middleware
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Add security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0", ".localhost", os.getenv("ALLOWED_HOST", "") or "*"]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [  # In production, replace with specific origins
        "http://localhost:3000",
        "http://localhost:8000",
        "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers for client-side access
    expose_headers=["X-Request-ID", "X-RateLimit-Remaining", "X-RateLimit-Limit"]
)

# Include API routes
app.include_router(router, prefix="/v1")

@app.get("/")
async def root():
    return {
        "message": "RAG Chatbot API is running!",
        "version": settings.app_version,
        "debug": settings.debug
    }

@app.get("/health")
async def health_check():
    """Health check endpoint with detailed status"""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": "development" if settings.debug else "production"
    }

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all requests"""
    request_id = request.headers.get("X-Request-ID", "unknown")
    logger.info("Request started",
                method=request.method,
                url=str(request.url),
                request_id=request_id)

    response = await call_next(request)

    logger.info("Request completed",
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                request_id=request_id)

    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error("Unhandled exception", error=str(exc), url=str(request.url))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "request_id": request.headers.get("X-Request-ID", "unknown")}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning"
    )