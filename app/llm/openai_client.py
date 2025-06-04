from base import BaseLLMClient
from openai import OpenAI
from typing import Generator

class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def chat(self, messages: list[dict], **kwargs) -> str:
        response = self.client.chat.completions.create(            
            messages=messages,
            **kwargs
        )
        return response

    def stream(self, messages: list[dict], **kwargs) -> Generator[str, None, None]:
        response = self.client.chat.completions.create(
            messages=messages,
            stream=True,
            **kwargs
        )
        return response 