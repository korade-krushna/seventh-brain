# Second Brain API

A personal knowledge base application using FastAPI, Milvus, and Gemini for storing and retrieving information using RAG (Retrieval Augmented Generation).

## Features

- Store questions and answers with vector embeddings
- Query the knowledge base using natural language
- Stream responses for real-time interaction
- Vector similarity search using Milvus
- RAG-powered responses using Gemini

## Prerequisites

- Python 3.8+
- Milvus server running locally or accessible
- Gemini API key

## Project Structure

```
app/
  ├── __init__.py
  ├── main.py
  ├── config.py
  ├── routes/
  │   ├── __init__.py
  │   ├── health.py
  │   └── knowledge.py
  └── services/
      ├── __init__.py
      ├── milvus_service.py
      └── gemini_service.py
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```bash
# Milvus Configuration
MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_COLLECTION_NAME=second_brain

# Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Vector Configuration
VECTOR_DIMENSION=768
VECTOR_INDEX_TYPE=IVF_FLAT
VECTOR_METRIC_TYPE=COSINE
```

## Running the Application

Start the server using uvicorn:
```bash
uvicorn app.main:app --reload
```

The application will be available at:
- http://localhost:8000
- API documentation: http://localhost:8000/docs

## API Endpoints

### Health Check
- GET `/health` - Check application health

### Knowledge Base
- POST `/knowledge/add` - Add a new document (question and answer)
- POST `/knowledge/query` - Query the knowledge base
- POST `/knowledge/query/stream` - Stream the response from querying

## Example Usage

1. Add a document:
```bash
curl -X POST "http://localhost:8000/knowledge/add" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is Python?", "answer": "Python is a high-level programming language..."}'
```

2. Query the knowledge base:
```bash
curl -X POST "http://localhost:8000/knowledge/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "Tell me about Python"}'
```

3. Stream query response:
```bash
curl -X POST "http://localhost:8000/knowledge/query/stream" \
     -H "Content-Type: application/json" \
     -d '{"question": "Tell me about Python"}'
``` 