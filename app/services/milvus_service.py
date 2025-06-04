from pymilvus import MilvusClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class MilvusService:
    """Service for handling Milvus vector database operations."""

    __client = None
    
    def __init__(self):
        """Initialize Milvus connection and collection."""
        self.connect()
        self.setup_collection()
    
    def connect(self):
        """Establish connection to Milvus server."""
        try:
            self.__client = MilvusClient("knowledge.db")
            logger.info("Successfully connected to Milvus")
        except Exception as e:
            logger.error(f"Failed to connect to Milvus: {e}")
            raise
    
    def setup_collection(self):
        """Setup or get existing collection with proper schema."""
        try:
            if not self.__client.has_collection(settings.MILVUS_COLLECTION_NAME):
                from pymilvus import CollectionSchema, FieldSchema, DataType
                fields = [
                    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                    FieldSchema(name="combined_question_answer", dtype=DataType.VARCHAR, max_length=50000),
                    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=settings.VECTOR_DIMENSION)
                ]
                schema = CollectionSchema(fields=fields)
                index_params = [{
                    "field_name": "embedding",
                    "index_type": settings.VECTOR_INDEX_TYPE,
                    "index_name": "embedding_index",
                    "metric_type": settings.VECTOR_METRIC_TYPE,
                    "params": {
                        "nlist": 768,
                        "nprobe": 10
                    }
                }]
                self.__client.create_collection(collection_name=settings.MILVUS_COLLECTION_NAME, schema=schema)
                self.__client.create_index(collection_name=settings.MILVUS_COLLECTION_NAME, index_params=index_params)
                logger.info(f"Created new collection: {settings.MILVUS_COLLECTION_NAME}")
            else:
                logger.info(f"Collection already exists: {settings.MILVUS_COLLECTION_NAME}")
        except Exception as e:
            logger.error(f"Failed to setup collection: {e}")
            raise
    
    def insert_document(self, combined_question_answer: str, embedding: list):
        """Insert a new document with its embedding into the collection."""
        try:
            entities = [
                {
                    "combined_question_answer": combined_question_answer,
                    "embedding": embedding
                }
            ]
            result = self.__client.insert(
                collection_name=settings.MILVUS_COLLECTION_NAME, 
                data=entities,
                partition_name="default"
            )
            logger.info(f"Successfully inserted document: {result}")
        except Exception as e:
            logger.error(f"Failed to insert document: {e}")
            raise
    
    def search_similar(self, query_embedding: list, top_k: int = 3):
        """Search for similar documents based on query embedding."""
        try:
            search_params = {
                "metric_type": settings.VECTOR_METRIC_TYPE,
                "params": {
                    "nprobe": 10,
                    "nlist": 768
                }
            }
            results = self.__client.search(
                collection_name=settings.MILVUS_COLLECTION_NAME,
                data=[query_embedding],
                anns_field="embedding",
                search_params=search_params,
                limit=top_k,
                output_fields=['combined_question_answer']
            )
            return results[0]
        except Exception as e:
            logger.error(f"Failed to search similar documents: {e}")
            raise
    
    def close(self):
        """Close the Milvus connection."""
        try:
            self.__client.close()
            logger.info("Successfully disconnected from Milvus")
        except Exception as e:
            logger.error(f"Failed to disconnect from Milvus: {e}")
            raise 