from base import BaseLLMClient
from google import genai
from typing import Generator

class GeminiClient(BaseLLMClient):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)

    def chat(self, messages: list[dict], **kwargs) -> str:
        response = self.client.models.generate_content(
            contents=[messages],
            **kwargs
        )
        return response

    def stream(self, messages: list[dict], **kwargs) -> Generator[str, None, None]:
        response = self.client.models.generate_content_stream(
            contents=[messages],
            **kwargs
        )
        return response