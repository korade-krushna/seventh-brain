from typing import AsyncGenerator
import google.generativeai as model
from app.config import settings
import logging
from google.generativeai import types
from google import genai
from google.genai import types

from app.constants import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for handling Gemini AI operations."""

    __client = None
   
    def __init__(self):
        """Initialize Gemini with API key."""
        self.__client = genai.Client(api_key=settings.GEMINI_API_KEY)
        logger.info("Successfully initialized Gemini service")
    
    async def get_embedding(self, text: str) -> list:
        """Generate embedding for the given text."""
        try:
            result = self.__client.models.embed_content(
                model="gemini-embedding-exp-03-07",
                contents=text,
                config=types.EmbedContentConfig(
                    task_type="SEMANTIC_SIMILARITY",
                    output_dimensionality=768
                    )
            )
            return result.embeddings[0].values
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise
    
    async def generate_response(self, question: str, context: list) -> str:
        """Generate response using RAG with the provided context."""
        try:
            context_str = "\n".join([
                f"Q: {item['question']}\nA: {item['answer']}"
                for item in context
            ])

            prompt = f"""
                Question: {question}
                
                Context:
                {context_str}
            """
            
            response = self.__client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[prompt],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            raise
    
    async def stream_response(self, question: str, context: list, tools: list) -> AsyncGenerator[str, None]:
        """Stream the response using RAG with the provided context."""
        try:
            context_str = "\n".join([
                f"Q: {item['question']}\nA: {item['answer']}"
                for item in context
            ])

            prompt = f"""
                Question: {question}
                
                Context:
                {context_str}
            """
            
            for chunk in self.__client.models.generate_content_stream(
                model='gemini-2.0-flash',
                contents=[prompt],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=tools  
                )
            ):
                text_chunk = chunk.text if hasattr(chunk, "text") else str(chunk)
                yield text_chunk
        except Exception as e:
            logger.error(f"Failed to stream response: {e}")
            raise 
    
    def get_model(self):
        return self.__client