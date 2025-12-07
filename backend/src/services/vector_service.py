from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional, Dict, Any
from src.config.settings import settings
from src.utils.logger import log_info, log_error, log_debug
import uuid

class VectorService:
    def __init__(self):
        # Initialize Qdrant client
        try:
            if settings.qdrant_api_key:
                self.client = QdrantClient(
                    url=settings.qdrant_host,
                    api_key=settings.qdrant_api_key,
                    prefer_grpc=True
                )
            else:
                # For local development without API key
                self.client = QdrantClient(host='localhost', port=6333)

            self.collection_name = settings.qdrant_collection_name
            self._connected = True
        except Exception as e:
            log_error(f"Could not connect to Qdrant: {str(e)}. Using fallback mode.")
            self._connected = False
            self.client = None

    def initialize_collection(self):
        """
        Initialize the Qdrant collection with the proper vector configuration
        """
        if not self._connected:
            log_info("Qdrant not connected, skipping collection initialization")
            return

        try:
            log_info(f"Initializing Qdrant collection: {self.collection_name}")

            # Check if collection already exists
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if self.collection_name not in collection_names:
                # Create collection with appropriate vector size for Gemini embeddings
                # Gemini embeddings are typically 768 dimensions
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=768,  # Standard size for Gemini embeddings
                        distance=models.Distance.COSINE
                    )
                )
                log_info(f"Created Qdrant collection: {self.collection_name}")
            else:
                log_info(f"Qdrant collection already exists: {self.collection_name}")

        except Exception as e:
            log_error(f"Error initializing Qdrant collection: {str(e)}")
            raise

    async def store_embedding(self, text: str, embedding: List[float], metadata: Dict[str, Any]) -> str:
        """
        Store an embedding with its associated metadata in Qdrant
        """
        if not self._connected:
            log_info("Qdrant not connected, skipping embedding storage")
            # Return a mock ID for development purposes
            return str(uuid.uuid4())

        try:
            log_info(f"Storing embedding in collection: {self.collection_name}")

            # Generate a unique ID for the vector
            vector_id = str(uuid.uuid4())

            # Upsert the point to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=vector_id,
                        vector=embedding,
                        payload={
                            "text": text,
                            **metadata  # Include all metadata fields
                        }
                    )
                ]
            )

            log_debug(f"Successfully stored embedding with ID: {vector_id}")
            return vector_id

        except Exception as e:
            log_error(f"Error storing embedding in Qdrant: {str(e)}")
            raise

    async def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors to the query embedding
        """
        if not self._connected:
            log_info("Qdrant not connected, returning empty search results")
            # Return empty results for development purposes
            return []

        try:
            log_info(f"Searching for similar vectors in collection: {self.collection_name}")

            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True
            )

            # Format results
            results = []
            for result in search_results:
                results.append({
                    "id": result.id,
                    "text": result.payload.get("text", ""),
                    "metadata": {k: v for k, v in result.payload.items() if k != "text"},
                    "score": result.score
                })

            log_debug(f"Found {len(results)} similar vectors")
            return results

        except Exception as e:
            log_error(f"Error searching for similar vectors in Qdrant: {str(e)}")
            raise

    async def delete_by_payload(self, payload_filter: Dict[str, Any]) -> int:
        """
        Delete vectors by payload filter
        """
        if not self._connected:
            log_info("Qdrant not connected, skipping vector deletion")
            # Return 0 for development purposes
            return 0

        try:
            log_info(f"Deleting vectors by payload filter in collection: {self.collection_name}")

            # Create filter based on payload
            filter_conditions = []
            for key, value in payload_filter.items():
                filter_conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    )
                )

            points_selector = models.FilterSelector(
                filter=models.Filter(
                    must=filter_conditions
                )
            )

            # Delete points
            result = self.client.delete(
                collection_name=self.collection_name,
                points_selector=points_selector
            )

            log_debug(f"Deleted vectors: {result}")
            return len(result.deleted) if hasattr(result, 'deleted') else 0

        except Exception as e:
            log_error(f"Error deleting vectors from Qdrant: {str(e)}")
            raise

# Global instance
vector_service = VectorService()