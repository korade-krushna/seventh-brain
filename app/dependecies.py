from app.services.milvus_service import MilvusService
from app.llm.llm import LLM
from app.tools.knowledge_functions import KnowledgeFunctions

class Dependencies:

    __milvus = None
    __llm = None
    __knowledge_functions = None

    def __init__(self):
        self.__milvus = MilvusService()
        self.__llm = LLM()
        self.__knowledge_functions = KnowledgeFunctions()
    def get_milvus(self):
        return self.__milvus
    
    def get_llm(self):
        return self.__llm.get_client()
    
    def get_knowledge_functions(self):
        return self.__knowledge_functions
