from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.content_chunk import ContentChunk
from src.utils.logger import log_info, log_error
import hashlib

class ContentChunkService:
    def __init__(self):
        pass

    def get_chunks_by_chapter(self, db: Session, chapter_id: str) -> List[ContentChunk]:
        """
        Retrieve all content chunks for a specific chapter
        """
        try:
            log_info(f"Retrieving chunks for chapter: {chapter_id}")
            chunks = db.query(ContentChunk).filter(ContentChunk.chapter_id == chapter_id).all()
            return chunks
        except Exception as e:
            log_error(f"Error retrieving chunks for chapter {chapter_id}: {str(e)}")
            raise

    def get_chunk_by_id(self, db: Session, chunk_id: str) -> Optional[ContentChunk]:
        """
        Retrieve a content chunk by its ID
        """
        try:
            log_info(f"Retrieving chunk with ID: {chunk_id}")
            chunk = db.query(ContentChunk).filter(ContentChunk.chunk_id == chunk_id).first()
            return chunk
        except Exception as e:
            log_error(f"Error retrieving chunk {chunk_id}: {str(e)}")
            raise

    def create_chunk(self, db: Session, chunk_data: dict) -> ContentChunk:
        """
        Create a new content chunk in the database
        """
        try:
            log_info(f"Creating chunk for chapter: {chunk_data.get('chapter_id')}")

            # Generate text hash if not provided
            text_hash = chunk_data.get('text_hash')
            if not text_hash:
                text_hash = hashlib.sha256(chunk_data['content'].encode()).hexdigest()

            # Create ContentChunk instance
            chunk = ContentChunk(
                chunk_id=chunk_data['chunk_id'],
                chapter_id=chunk_data['chapter_id'],
                content=chunk_data['content'],
                char_offset=chunk_data['char_offset'],
                length=chunk_data['length'],
                source_url=chunk_data.get('source_url'),
                text_hash=text_hash,
                embedding_vector_id=chunk_data.get('embedding_vector_id')
            )

            db.add(chunk)
            db.commit()
            db.refresh(chunk)

            log_info(f"Successfully created chunk: {chunk.chunk_id}")
            return chunk
        except Exception as e:
            log_error(f"Error creating chunk: {str(e)}")
            db.rollback()
            raise

    def create_chunks_batch(self, db: Session, chunks_data: List[dict]) -> List[ContentChunk]:
        """
        Create multiple content chunks in a batch
        """
        try:
            log_info(f"Creating batch of {len(chunks_data)} chunks")
            created_chunks = []

            for chunk_data in chunks_data:
                # Generate text hash if not provided
                text_hash = chunk_data.get('text_hash')
                if not text_hash:
                    text_hash = hashlib.sha256(chunk_data['content'].encode()).hexdigest()

                chunk = ContentChunk(
                    chunk_id=chunk_data['chunk_id'],
                    chapter_id=chunk_data['chapter_id'],
                    content=chunk_data['content'],
                    char_offset=chunk_data['char_offset'],
                    length=chunk_data['length'],
                    source_url=chunk_data.get('source_url'),
                    text_hash=text_hash,
                    embedding_vector_id=chunk_data.get('embedding_vector_id')
                )
                created_chunks.append(chunk)

            db.add_all(created_chunks)
            db.commit()

            # Refresh all created chunks
            for chunk in created_chunks:
                db.refresh(chunk)

            log_info(f"Successfully created {len(created_chunks)} chunks in batch")
            return created_chunks
        except Exception as e:
            log_error(f"Error creating chunks batch: {str(e)}")
            db.rollback()
            raise

    def update_chunk_embedding_id(self, db: Session, chunk_id: str, embedding_id: str) -> bool:
        """
        Update the embedding vector ID for a specific chunk
        """
        try:
            log_info(f"Updating embedding ID for chunk: {chunk_id}")

            chunk = db.query(ContentChunk).filter(ContentChunk.chunk_id == chunk_id).first()
            if not chunk:
                return False

            chunk.embedding_vector_id = embedding_id
            db.commit()
            db.refresh(chunk)

            log_info(f"Successfully updated embedding ID for chunk: {chunk_id}")
            return True
        except Exception as e:
            log_error(f"Error updating embedding ID for chunk {chunk_id}: {str(e)}")
            db.rollback()
            raise

    def delete_chunks_by_chapter(self, db: Session, chapter_id: str) -> int:
        """
        Delete all content chunks for a specific chapter
        """
        try:
            log_info(f"Deleting all chunks for chapter: {chapter_id}")

            chunks = db.query(ContentChunk).filter(ContentChunk.chapter_id == chapter_id).all()
            count = len(chunks)

            for chunk in chunks:
                db.delete(chunk)

            db.commit()

            log_info(f"Successfully deleted {count} chunks for chapter: {chapter_id}")
            return count
        except Exception as e:
            log_error(f"Error deleting chunks for chapter {chapter_id}: {str(e)}")
            db.rollback()
            raise

# Global instance
content_chunk_service = ContentChunkService()