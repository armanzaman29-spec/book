from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.chapter import Chapter
from src.models.content_chunk import ContentChunk
from src.utils.logger import log_info, log_error

class ChapterService:
    def __init__(self):
        pass

    def get_all_chapters(self, db: Session) -> List[Chapter]:
        """
        Retrieve all chapters from the database
        """
        try:
            log_info("Retrieving all chapters")
            chapters = db.query(Chapter).all()
            return chapters
        except Exception as e:
            log_error(f"Error retrieving chapters: {str(e)}")
            raise

    def get_chapter_by_id(self, db: Session, chapter_id: str) -> Optional[Chapter]:
        """
        Retrieve a chapter by its ID
        """
        try:
            log_info(f"Retrieving chapter with ID: {chapter_id}")
            chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
            return chapter
        except Exception as e:
            log_error(f"Error retrieving chapter {chapter_id}: {str(e)}")
            raise

    def create_chapter(self, db: Session, chapter_data: dict) -> Chapter:
        """
        Create a new chapter in the database
        """
        try:
            log_info(f"Creating chapter with ID: {chapter_data.get('chapter_id')}")

            # Create Chapter instance
            chapter = Chapter(
                chapter_id=chapter_data['chapter_id'],
                title=chapter_data['title'],
                content=chapter_data['content'],
                learning_objectives=chapter_data.get('learning_objectives'),
                apa_references=chapter_data.get('apa_references'),
                chunking_strategy=chapter_data.get('chunking_strategy', 'paragraph'),
                embedding_ready=chapter_data.get('embedding_ready', False)
            )

            db.add(chapter)
            db.commit()
            db.refresh(chapter)

            log_info(f"Successfully created chapter: {chapter.title}")
            return chapter
        except Exception as e:
            log_error(f"Error creating chapter: {str(e)}")
            db.rollback()
            raise

    def update_chapter(self, db: Session, chapter_id: str, chapter_data: dict) -> Optional[Chapter]:
        """
        Update an existing chapter
        """
        try:
            log_info(f"Updating chapter with ID: {chapter_id}")

            chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
            if not chapter:
                return None

            # Update fields if provided
            if 'title' in chapter_data:
                chapter.title = chapter_data['title']
            if 'content' in chapter_data:
                chapter.content = chapter_data['content']
            if 'learning_objectives' in chapter_data:
                chapter.learning_objectives = chapter_data['learning_objectives']
            if 'apa_references' in chapter_data:
                chapter.apa_references = chapter_data['apa_references']
            if 'chunking_strategy' in chapter_data:
                chapter.chunking_strategy = chapter_data['chunking_strategy']
            if 'embedding_ready' in chapter_data:
                chapter.embedding_ready = chapter_data['embedding_ready']

            db.commit()
            db.refresh(chapter)

            log_info(f"Successfully updated chapter: {chapter.title}")
            return chapter
        except Exception as e:
            log_error(f"Error updating chapter {chapter_id}: {str(e)}")
            db.rollback()
            raise

    def delete_chapter(self, db: Session, chapter_id: str) -> bool:
        """
        Delete a chapter by its ID
        """
        try:
            log_info(f"Deleting chapter with ID: {chapter_id}")

            chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
            if not chapter:
                return False

            db.delete(chapter)
            db.commit()

            log_info(f"Successfully deleted chapter: {chapter_id}")
            return True
        except Exception as e:
            log_error(f"Error deleting chapter {chapter_id}: {str(e)}")
            db.rollback()
            raise

# Global instance
chapter_service = ChapterService()