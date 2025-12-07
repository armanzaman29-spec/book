from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.main import api_router
from src.config.settings import settings
from src.services.vector_service import vector_service
from src.utils.logger import log_info, log_error

# Initialize the FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for the AI-Native Textbook with RAG chatbot functionality",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    """
    Initialize services on startup
    """
    log_info("Starting up Textbook RAG API")

    # Initialize the vector service collection
    try:
        vector_service.initialize_collection()
        log_info("Vector service initialized successfully")
    except Exception as e:
        log_error(f"Error initializing vector service: {str(e)}")
        # Don't raise the exception to allow the app to start even without Qdrant
        log_info("Continuing startup without Qdrant connection")

@app.get("/")
async def root():
    """
    Root endpoint to check if the API is running
    """
    return {
        "message": "Textbook RAG API is running",
        "version": settings.app_version,
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Textbook RAG API",
        "version": settings.app_version
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )