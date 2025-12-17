import os
import asyncio
import json
from typing import List, Dict, Any, Tuple, Optional
from openai import OpenAI
from pydantic import BaseModel
from retrieving import VectorDBRetriever
from dotenv import load_dotenv
import structlog
from config import settings
from tenacity import retry, stop_after_attempt, wait_exponential
import time
from logging_config import get_logger_instance
import httpx

# Load environment variables
load_dotenv()

logger = get_logger_instance()

class RAGAgent:
    def __init__(self, retriever: VectorDBRetriever):
        """
        Initialize the RAG agent with a vector database retriever
        """
        self.retriever = retriever

        # Get API keys from settings
        self.openai_api_key = settings.openai_api_key
        self.groq_api_key = settings.groq_api_key

        # Initialize clients based on available API keys
        if self.groq_api_key:
            # Use Groq API
            self.client = OpenAI(
                api_key=self.groq_api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = "llama-3.1-8b-instant"  # Using the correct model name for Groq
            self.api_type = "groq"
        elif self.openai_api_key:
            # Fallback to OpenAI API
            self.client = OpenAI(api_key=self.openai_api_key)
            self.model = settings.openai_model
            self.api_type = "openai"
        else:
            raise ValueError("Either OPENAI_API_KEY or GROQ_API_KEY must be set in environment variables")

    async def is_healthy(self) -> bool:
        """
        Check if the agent is healthy by testing the API connection
        """
        try:
            # Test API connection by making a simple call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "health check"}],
                max_tokens=5,
                temperature=0.0
            )

            if response.choices and len(response.choices) > 0:
                logger.info(f"Agent health check passed for {self.api_type} API")
                return True
            else:
                logger.error("Agent health check failed: no response")
                return False
        except Exception as e:
            logger.error("Agent health check failed", error=str(e))
            return False

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def process_query(
        self,
        query: str,
        messages: List[Dict[str, Any]],
        max_tokens: int = 500,
        temperature: float = 0.7,
        top_k: int = 5
    ) -> Tuple[str, List[str], List[str]]:
        """
        Process a user query using RAG approach with retry logic

        Args:
            query: The user's query
            messages: Conversation history
            max_tokens: Maximum tokens for the response
            temperature: Temperature for response creativity
            top_k: Number of documents to retrieve

        Returns:
            Tuple of (response, context, sources)
        """
        start_time = time.time()
        log = logger.bind(query=query[:50])

        try:
            log.info("Starting query processing")

            # Retrieve relevant context from the vector database
            context, sources = await self.retriever.get_relevant_context(query, top_k)

            # Build the system message with retrieved context
            system_message_content = f"""
            You are an expert AI assistant that uses retrieved context to answer questions.
            Use the following retrieved context to answer the user's question:

            Retrieved Context:
            {' '.join(context)}

            Instructions:
            1. Answer based on the provided context when possible
            2. If the context doesn't contain enough information, acknowledge this limitation
            3. Be concise, accurate, and helpful in your response
            4. If citing sources, refer to them generally without specific IDs
            5. Maintain a professional and friendly tone
            6. If the question is ambiguous, ask for clarification
            """

            # Prepare the messages for the OpenAI API
            prepared_messages = [
                {"role": "system", "content": system_message_content}
            ]

            # Add conversation history (excluding the current query which is in 'query' parameter)
            for msg in messages:
                prepared_messages.append({"role": msg["role"], "content": msg["content"]})

            # Add the current query
            prepared_messages.append({"role": "user", "content": query})

            # Call the OpenAI API to generate a response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=prepared_messages,
                max_tokens=max_tokens,
                temperature=temperature
            )

            # Extract the response text
            response_text = response.choices[0].message.content.strip()

            processing_time = time.time() - start_time
            log.info("Query processed successfully",
                    processing_time=processing_time,
                    context_count=len(context),
                    sources_count=len(sources))

            return response_text, context, sources

        except Exception as e:
            processing_time = time.time() - start_time
            log.error("Error processing query", error=str(e), processing_time=processing_time)
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_response_with_context(
        self,
        query: str,
        context: List[str],
        conversation_history: List[Dict[str, str]] = None,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """
        Generate a response using the provided context and conversation history with retry logic
        """
        start_time = time.time()
        log = logger.bind(query=query[:50])

        try:
            log.info("Generating response with context")

            system_prompt = f"""
            You are an expert AI assistant that helps users by answering questions based on provided context.
            Context:
            {' '.join(context)}

            Instructions:
            - Answer the user's question using only the provided context when possible
            - If the context doesn't contain sufficient information, acknowledge this politely
            - Be concise, accurate, and helpful
            - Maintain a professional and friendly tone
            - Structure your response clearly
            """

            messages = [{"role": "system", "content": system_prompt}]

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add the user query
            messages.append({"role": "user", "content": query})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )

            processing_time = time.time() - start_time
            log.info("Response generated successfully", processing_time=processing_time)

            return response.choices[0].message.content.strip()

        except Exception as e:
            processing_time = time.time() - start_time
            log.error("Error generating response with context", error=str(e), processing_time=processing_time)
            raise

    async def answer_question(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        High-level method to answer a question using RAG
        """
        start_time = time.time()
        log = logger.bind(query=query[:50])

        try:
            log.info("Answering question with RAG")

            # Retrieve relevant documents
            context, sources = await self.retriever.get_relevant_context(query, top_k)

            # Generate answer using the context
            answer = await self.generate_response_with_context(query, context)

            processing_time = time.time() - start_time
            log.info("Question answered successfully", processing_time=processing_time)

            return {
                "answer": answer,
                "context": context,
                "sources": sources,
                "processing_time": processing_time,
                "model_used": self.model
            }

        except Exception as e:
            processing_time = time.time() - start_time
            log.error("Error answering question", error=str(e), processing_time=processing_time)
            raise

    async def stream_response(
        self,
        query: str,
        messages: List[Dict[str, Any]],
        max_tokens: int = 500,
        temperature: float = 0.7,
        top_k: int = 5
    ):
        """
        Stream response from the agent (for real-time responses)
        """
        # Retrieve relevant context
        context, sources = await self.retriever.get_relevant_context(query, top_k)

        # Build the system message with retrieved context
        system_message_content = f"""
        You are an expert AI assistant that uses retrieved context to answer questions.
        Use the following retrieved context to answer the user's question:

        Retrieved Context:
        {' '.join(context)}

        Instructions:
        1. Answer based on the provided context when possible
        2. If the context doesn't contain enough information, acknowledge this limitation
        3. Be concise, accurate, and helpful in your response
        4. If citing sources, refer to them generally without specific IDs
        5. Maintain a professional and friendly tone
        """

        # Prepare the messages for the OpenAI API
        prepared_messages = [
            {"role": "system", "content": system_message_content}
        ]

        # Add conversation history
        for msg in messages:
            prepared_messages.append({"role": msg["role"], "content": msg["content"]})

        # Add the current query
        prepared_messages.append({"role": "user", "content": query})

        # Create streaming response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=prepared_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )

        # Yield each chunk as it arrives
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def get_query_analysis(self, query: str) -> Dict[str, Any]:
        """
        Analyze a query to understand its intent and complexity
        """
        try:
            analysis_prompt = f"""
            Analyze the following query and provide structured information:

            Query: {query}

            Provide the following analysis:
            1. Intent: What is the user trying to achieve?
            2. Complexity: How complex is this query? (simple, moderate, complex)
            3. Category: What category does this query fall into?
            4. Keywords: What are the key terms in this query?
            5. Expected response type: What kind of response is the user looking for?

            Respond in JSON format with the keys: intent, complexity, category, keywords, expected_response_type
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": analysis_prompt}],
                max_tokens=300,
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            import json
            analysis = json.loads(response.choices[0].message.content.strip())

            return {
                "query": query,
                "analysis": analysis,
                "model_used": self.model
            }

        except Exception as e:
            logger.error("Error analyzing query", error=str(e))
            # Return a default analysis in case of error
            return {
                "query": query,
                "analysis": {
                    "intent": "unknown",
                    "complexity": "moderate",
                    "category": "general",
                    "keywords": query.split()[:5],
                    "expected_response_type": "explanation"
                },
                "model_used": self.model
            }

class MultiAgentOrchestrator:
    """
    Orchestrates multiple agents for complex queries
    """
    def __init__(self, retriever: VectorDBRetriever):
        self.rag_agent = RAGAgent(retriever)
        self.agents = {
            "rag": self.rag_agent
        }

    async def route_query(self, query: str) -> str:
        """
        Determine which agent should handle the query
        """
        # For now, all queries go to RAG agent
        # In a more complex system, this could route to different agents
        # based on query analysis
        analysis = await self.rag_agent.get_query_analysis(query)
        return "rag"

    async def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Process a query using the appropriate agent
        """
        agent_type = await self.route_query(query)
        agent = self.agents[agent_type]

        return await agent.answer_question(query, **kwargs)