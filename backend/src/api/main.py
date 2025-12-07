from fastapi import APIRouter
from src.api import ingest, embed, query, select_query

# Main API router
api_router = APIRouter()

# Include API routes
api_router.include_router(ingest.router, prefix="/v1", tags=["ingest"])
api_router.include_router(embed.router, prefix="/v1", tags=["embed"])
api_router.include_router(query.router, prefix="/v1", tags=["query"])
api_router.include_router(select_query.router, prefix="/v1", tags=["select-query"])