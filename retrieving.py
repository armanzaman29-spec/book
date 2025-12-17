import os
import asyncio
import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, SearchParams
from qdrant_client.http import models
import cohere
from dotenv import load_dotenv
import structlog
import redis
from config import settings
from tenacity import retry, stop_after_attempt, wait_exponential
from logging_config import get_logger_instance

# Load environment variables
load_dotenv()

logger = get_logger_instance()

class VectorDBRetriever:
    def __init__(self):
        """
        Initialize the vector database retriever with Qdrant and Cohere
        """
        self.qdrant_url = settings.qdrant_url
        self.qdrant_api_key = settings.qdrant_api_key

        if not self.qdrant_url or not self.qdrant_api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in environment variables")

        self.client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            prefer_grpc=False  # Using REST API
        )

        # Initialize Cohere client for embeddings
        self.cohere_api_key = settings.cohere_api_key
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY must be set in environment variables")

        self.cohere_client = cohere.Client(self.cohere_api_key)

        # Collection name for storing documents
        self.collection_name = settings.qdrant_collection_name

        # Initialize Redis for caching
        try:
            self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            self.use_cache = True
        except Exception as e:
            logger.warning("Redis connection failed, caching disabled", error=str(e))
            self.use_cache = False

        # Initialize the collection if it doesn't exist
        self._initialize_collection()

    def _initialize_collection(self):
        """
        Initialize the Qdrant collection for storing document embeddings
        """
        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if self.collection_name not in collection_names:
                # Create a new collection with Cohere embedding dimensions (usually 1024)
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")

        except Exception as e:
            logger.error(f"Error initializing collection: {e}")
            raise

    def _generate_cache_key(self, query: str, top_k: int) -> str:
        """
        Generate a cache key for the query
        """
        cache_input = f"{query}:{top_k}:{self.collection_name}"
        return f"rag_cache:{hashlib.md5(cache_input.encode()).hexdigest()}"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embeddings for a text using Cohere with retry logic
        """
        try:
            response = self.cohere_client.embed(
                texts=[text],
                model=settings.cohere_model
            )
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts with retry logic
        """
        try:
            response = self.cohere_client.embed(
                texts=texts,
                model=settings.cohere_model
            )
            return response.embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    async def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None):
        """
        Add a document to the vector database
        """
        try:
            # Generate embedding for the content
            embedding = self.embed_text(content)

            # Prepare the point for Qdrant
            point = PointStruct(
                id=doc_id,
                vector=embedding,
                payload={
                    "content": content,
                    "metadata": metadata or {}
                }
            )

            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            logger.info(f"Document {doc_id} added successfully")
            return True

        except Exception as e:
            logger.error(f"Error adding document {doc_id}: {e}")
            raise

    async def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Add multiple documents to the vector database
        """
        try:
            # Extract content for embedding
            texts = [doc["content"] for doc in documents]

            # Generate embeddings for all texts at once (more efficient)
            embeddings = self.embed_texts(texts)

            # Prepare points for Qdrant
            points = []
            for i, doc in enumerate(documents):
                point = PointStruct(
                    id=doc["id"],
                    vector=embeddings[i],
                    payload={
                        "content": doc["content"],
                        "metadata": doc.get("metadata", {})
                    }
                )
                points.append(point)

            # Upload all points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"{len(documents)} documents added successfully")
            return True

        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant documents based on the query with retry logic
        """
        try:
            # Check cache first if available
            if self.use_cache:
                cache_key = self._generate_cache_key(query, top_k)
                cached_result = self.redis_client.get(cache_key)
                if cached_result:
                    logger.info("Cache hit for search query")
                    return json.loads(cached_result)

            # Generate embedding for the query
            query_embedding = self.embed_text(query)

            # Search in Qdrant
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True
            )

            # Format results
            results = []
            for hit in search_result:
                results.append({
                    "id": hit.id,
                    "content": hit.payload["content"],
                    "metadata": hit.payload.get("metadata", {}),
                    "score": hit.score
                })

            logger.info(f"Found {len(results)} results for query")

            # Cache the results if cache is enabled
            if self.use_cache:
                try:
                    self.redis_client.setex(
                        cache_key,
                        settings.cache_ttl_seconds,
                        json.dumps(results, default=str)
                    )
                except Exception as e:
                    logger.warning("Failed to cache search results", error=str(e))

            return results

        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise

    async def get_relevant_context(self, query: str, top_k: int = 3) -> tuple[List[str], List[str]]:
        """
        Get relevant context and sources for a query
        Returns: (context_list, source_list)
        """
        try:
            search_results = await self.search(query, top_k)

            context = [result["content"] for result in search_results]
            sources = [str(result["id"]) for result in search_results]

            return context, sources

        except Exception as e:
            logger.error(f"Error getting relevant context: {e}")
            # Return empty context instead of raising an exception to allow the agent to still function
            return [], []

    async def health_check(self) -> bool:
        """
        Perform a health check on the retriever
        """
        try:
            # Test Cohere connection by generating a simple embedding first (this is faster)
            test_embedding = self.embed_text("health check")

            if len(test_embedding) > 0:
                logger.info("Retriever health check passed (Cohere working)")
                return True
            else:
                logger.error("Retriever health check failed: empty embedding")
                return False

        except Exception as e:
            logger.warning("Retriever health check: Cohere failed, but that's OK for basic functionality", error=str(e))
            return False  # Return False if Cohere is not working either

    async def clear_cache(self):
        """
        Clear the Redis cache
        """
        if self.use_cache:
            try:
                # Delete all keys with the rag_cache prefix
                cache_keys = self.redis_client.keys("rag_cache:*")
                if cache_keys:
                    self.redis_client.delete(*cache_keys)
                logger.info(f"Cleared {len(cache_keys)} cache entries")
            except Exception as e:
                logger.error("Failed to clear cache", error=str(e))

    async def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the vector database
        """
        try:
            # Delete from Qdrant
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[doc_id]
            )

            # Clear cache
            await self.clear_cache()

            logger.info(f"Document {doc_id} deleted successfully")
            return True

        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")
            raise

    async def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "vectors_count": collection_info.vectors_count,
                "indexed_vectors_count": collection_info.indexed_vectors_count,
                "points_count": collection_info.points_count
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            raise