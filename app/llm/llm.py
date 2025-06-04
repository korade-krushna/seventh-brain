from base import BaseLLMClient
from openai_client import OpenAIClient
from gemini_client import GeminiClient
from ollma_client import OllamaClient
import os

class LLM:

    __client: BaseLLMClient = None

    def __init__(self):
        OPENAI_KEY = os.getenv("OPENAI_KEY")
        GEMINI_KEY = os.getenv("GEMINI_KEY")
        OLLAMA_HOST = os.getenv("OLLAMA_HOST")
        if OPENAI_KEY:
            self.__client = OpenAIClient(OPENAI_KEY)
        elif GEMINI_KEY:
            self.__client = GeminiClient(GEMINI_KEY)
        elif OLLAMA_HOST:
            self.__client = OllamaClient()
        else:
            raise ValueError("No LLM client found")

    def get_client(self) -> BaseLLMClient:
        return self.__client