from app.services.milvus_service import MilvusService
from app.services.gemini_service import GeminiService
import logging
from google.genai.types import FunctionCall

class KnowledgeFunctions:

    def __init__(self):
        self.logger = logging.getLogger(__name__)  
        self.milvus = MilvusService()
        self.gemini = GeminiService()


    query_knowledge_base_tool_spec = {
        "name": "query_knowledge_base",
        "description": "Query the knowledge base for relevant information about the user's question.",
        "parameters": {
            "type": "object",  # Correct type
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The user's query to search for in the knowledge base."
                }
            },
            "required": ["query"]
        }
    }

    async def query_knowledge_base(self, query: str) -> str:
        """Query the knowledge base and get a response."""
        try:
            query_embedding = await self.gemini.get_embedding(query)
            similar_docs = self.milvus.search_similar(query_embedding)
            context = [doc['combined_question_answer'] for doc in similar_docs if doc['distance'] > 0.8]
            if len(context) == 0:
                return "No relevant information found in the knowledge base."
            return "\n\n".join(context)
        except Exception as e:
            self.logger.error(f"Failed to query knowledge base: {e}")
            raise
    

    async def call_tool(self, function_call: FunctionCall) -> str:
        """Call the tool and get a response."""
        if function_call.name == 'query_knowledge_base':
            return await self.query_knowledge_base(**function_call.args)
        else:
            raise ValueError(f"Unknown tool: {function_call.name}")
