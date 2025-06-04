from pydantic import BaseModel
from pydantic import Field

class DocumentInput(BaseModel):
    """Input model for adding a new document, all fields are required."""
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)


class QueryInput(BaseModel):
    """Input model for querying the knowledge base."""
    question: str

class Session(BaseModel):
    """Model for a session."""
    id: str
    user_id: str
    name: str
    content: list[dict]
    created_at: int
    updated_at: int
