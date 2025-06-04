from base import BaseLLMClient
from ollama import chat
from typing import Generator

class OllamaClient(BaseLLMClient):
    def __init__(self):
        pass

    def chat(self, messages: list[dict], **kwargs) -> str:
        response = chat(
            messages=messages,
            **kwargs
        )
        return response

    def stream(self, messages: list[dict], **kwargs) -> Generator[str, None, None]:
        response = chat(
            messages=messages,
            stream=True,
            **kwargs
        )
        return response