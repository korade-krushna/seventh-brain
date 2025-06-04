from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Milvus Configuration
    MILVUS_HOST: str = Field(default="localhost", env="MILVUS_HOST")
    MILVUS_PORT: int = Field(default=19530, env="MILVUS_PORT")
    MILVUS_COLLECTION_NAME: str = Field(default="knowledge", env="MILVUS_COLLECTION_NAME")
    
    # Gemini Configuration
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    
    # Vector Configuration
    VECTOR_DIMENSION: int = Field(default=768, env="VECTOR_DIMENSION")
    VECTOR_INDEX_TYPE: str = Field(default="IVF_FLAT", env="VECTOR_INDEX_TYPE")
    VECTOR_METRIC_TYPE: str = Field(default="COSINE", env="VECTOR_METRIC_TYPE")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 