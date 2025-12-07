import google.generativeai as genai
from typing import List, Optional, Dict, Any
from src.config.settings import settings
from src.utils.logger import log_info, log_error, log_debug

class GeminiService:
    def __init__(self):
        # Configure the API key
        genai.configure(api_key=settings.gemini_api_key)

        # Initialize the generative model
        self.model = genai.GenerativeModel(settings.gemini_model_name)

        # Initialize the embedding model
        self.embedding_model = settings.embedding_model_name

    async def generate_text(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate text using the Gemini model
        """
        try:
            log_info(f"Generating text with model: {settings.gemini_model_name}")

            # Prepare the full prompt with context if provided
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nQuestion: {prompt}"

            # Generate content
            response = await self.model.generate_content_async(full_prompt)

            if response and response.text:
                log_debug("Text generation completed successfully")
                return response.text.strip()
            else:
                log_error("No text returned from Gemini API")
                return "I couldn't generate a response. Please try again."

        except Exception as e:
            log_error(f"Error in Gemini text generation: {str(e)}")
            raise

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for the given text using the embedding model
        """
        try:
            log_info(f"Generating embedding with model: {self.embedding_model}")

            # Generate embedding
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"  # Appropriate for RAG documents
            )

            if result and 'embedding' in result:
                log_debug("Embedding generation completed successfully")
                return result['embedding']
            else:
                log_error("No embedding returned from Gemini API")
                raise Exception("Embedding generation failed")

        except Exception as e:
            log_error(f"Error in Gemini embedding generation: {str(e)}")
            raise

    async def batch_generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        """
        embeddings = []
        for text in texts:
            embedding = await self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings

# Global instance
gemini_service = GeminiService()