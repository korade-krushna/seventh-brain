from abc import ABC, abstractmethod

class BaseLLMClient(ABC):

    @abstractmethod
    def chat(self, messages: list[dict], **kwargs) -> str:
        pass

    @abstractmethod
    def stream(self, messages: list[dict], **kwargs) -> str:
        pass
