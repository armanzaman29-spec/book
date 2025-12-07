from typing import List, Dict, Any, Optional
from src.services.gemini_service import gemini_service
from src.services.vector_service import vector_service
from src.services.content_chunk_service import content_chunk_service
from sqlalchemy.orm import Session
from src.models.content_chunk import ContentChunk
from src.utils.logger import log_info, log_error, log_debug
import time

class RAGService:
    def __init__(self):
        self.gemini_service = gemini_service
        self.vector_service = vector_service
        self.content_chunk_service = content_chunk_service

    async def query(self, db: Session, question: str, user_id: Optional[str] = None, max_sources: int = 3) -> Dict[str, Any]:
        """
        Perform a RAG query against textbook content
        """
        try:
            log_info(f"Processing RAG query: {question[:50]}...")
            start_time = time.time()

            # Generate embedding for the question
            query_embedding = await self.gemini_service.generate_embedding(question)

            # Search for similar content in the vector store
            similar_chunks = await self.vector_service.search_similar(
                query_embedding=query_embedding,
                limit=max_sources
            )

            if not similar_chunks:
                log_debug("No similar content found, generating general response")
                answer = await self.gemini_service.generate_text(question)
                response_time = time.time() - start_time
                return {
                    "answer": answer,
                    "sources": [],
                    "confidence": 0.5,  # Default confidence when no sources found
                    "query_id": f"query_{int(time.time())}",
                    "response_time_ms": int(response_time * 1000)
                }

            # Prepare context from the retrieved chunks
            context_parts = []
            sources = []
            for chunk in similar_chunks:
                context_parts.append(chunk["text"])
                sources.append({
                    "chunk_id": chunk["id"],
                    "text_preview": chunk["text"][:100] + "..." if len(chunk["text"]) > 100 else chunk["text"],
                    "metadata": chunk["metadata"]
                })

            context = "\n\n".join(context_parts)

            # Generate answer using the context and question
            answer = await self.gemini_service.generate_text(question, context)

            response_time = time.time() - start_time

            # Calculate confidence based on similarity scores
            avg_similarity = sum([chunk["score"] for chunk in similar_chunks]) / len(similar_chunks) if similar_chunks else 0
            confidence = min(1.0, avg_similarity * 2)  # Normalize to 0-1 range

            result = {
                "answer": answer,
                "sources": sources,
                "confidence": confidence,
                "query_id": f"query_{int(time.time())}",
                "response_time_ms": int(response_time * 1000)
            }

            log_debug(f"RAG query completed in {result['response_time_ms']}ms with {len(sources)} sources")
            return result

        except Exception as e:
            log_error(f"Error in RAG query: {str(e)}")
            raise

    async def selection_query(self, selected_text: str, question: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform a selection-only query using only the provided text
        """
        try:
            log_info(f"Processing selection-only query for text excerpt: {selected_text[:50]}...")
            start_time = time.time()

            # Generate answer using only the selected text as context
            answer = await self.gemini_service.generate_text(question, selected_text)

            response_time = time.time() - start_time

            # For selection-only mode, we can be more confident since we're using exact text
            confidence = 0.9

            result = {
                "answer": answer,
                "sources": [{
                    "text_preview": selected_text[:100] + "..." if len(selected_text) > 100 else selected_text,
                    "type": "selected_text"
                }],
                "confidence": confidence,
                "query_id": f"sel_query_{int(time.time())}",
                "response_time_ms": int(response_time * 1000)
            }

            log_debug(f"Selection-only query completed in {result['response_time_ms']}ms")
            return result

        except Exception as e:
            log_error(f"Error in selection-only query: {str(e)}")
            raise

    async def ingest_content(self, db: Session, chapter_id: str, content: str, chunk_size: int = 1000) -> Dict[str, Any]:
        """
        Ingest content for a chapter and prepare it for embedding
        """
        try:
            log_info(f"Ingesting content for chapter: {chapter_id}")

            # Simple chunking strategy - split by paragraphs and ensure chunks are not too large
            paragraphs = content.split('\n\n')
            chunks = []
            chunk_id_counter = 1

            char_position = 0
            for paragraph in paragraphs:
                # If paragraph is too large, split it further
                if len(paragraph) > chunk_size:
                    sub_chunks = [paragraph[i:i+chunk_size] for i in range(0, len(paragraph), chunk_size)]
                    for sub_chunk in sub_chunks:
                        chunk_data = {
                            'chunk_id': f"{chapter_id}_chunk_{chunk_id_counter}",
                            'chapter_id': chapter_id,
                            'content': sub_chunk,
                            'char_offset': char_position,
                            'length': len(sub_chunk),
                            'source_url': f"/docs/{chapter_id}"
                        }
                        chunks.append(chunk_data)
                        char_position += len(sub_chunk)
                        chunk_id_counter += 1
                else:
                    chunk_data = {
                        'chunk_id': f"{chapter_id}_chunk_{chunk_id_counter}",
                        'chapter_id': chapter_id,
                        'content': paragraph,
                        'char_offset': char_position,
                        'length': len(paragraph),
                        'source_url': f"/docs/{chapter_id}"
                    }
                    chunks.append(chunk_data)
                    char_position += len(paragraph)
                    chunk_id_counter += 1

            # Save chunks to database
            created_chunks = self.content_chunk_service.create_chunks_batch(db, chunks)

            result = {
                "status": "success",
                "processed_chunks": len(created_chunks),
                "message": f"Successfully ingested {len(created_chunks)} chunks for chapter {chapter_id}"
            }

            log_info(f"Ingestion completed: {result['message']}")
            return result

        except Exception as e:
            log_error(f"Error in content ingestion: {str(e)}")
            raise

    async def generate_embeddings(self, db: Session, chunk_ids: List[str]) -> Dict[str, Any]:
        """
        Generate embeddings for specific content chunks
        """
        try:
            log_info(f"Generating embeddings for {len(chunk_ids)} chunks")

            # Get chunks from database
            chunks_to_process = []
            for chunk_id in chunk_ids:
                # This would need to be implemented differently since we can't query by individual IDs efficiently
                # For now, we'll process them one by one
                chunk = self.content_chunk_service.get_chunk_by_id(db, chunk_id)
                if chunk:
                    chunks_to_process.append(chunk)

            processed_count = 0
            for chunk in chunks_to_process:
                # Generate embedding for the chunk content
                embedding = await self.gemini_service.generate_embedding(chunk.content)

                # Store the embedding in the vector store
                vector_id = await self.vector_service.store_embedding(
                    text=chunk.content,
                    embedding=embedding,
                    metadata={
                        "chunk_id": chunk.chunk_id,
                        "chapter_id": chunk.chapter_id,
                        "char_offset": chunk.char_offset,
                        "source_url": chunk.source_url
                    }
                )

                # Update the chunk with the embedding vector ID
                self.content_chunk_service.update_chunk_embedding_id(db, chunk.chunk_id, vector_id)
                processed_count += 1

            result = {
                "status": "success",
                "embedded_chunks": processed_count,
                "message": f"Successfully generated embeddings for {processed_count} chunks"
            }

            log_info(f"Embedding generation completed: {result['message']}")
            return result

        except Exception as e:
            log_error(f"Error in embedding generation: {str(e)}")
            raise

# Global instance
rag_service = RAGService()