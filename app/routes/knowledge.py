from google.genai import types
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field, constr
from typing import List, AsyncGenerator
import logging
from app.constants import SYSTEM_PROMPT
from app.models import DocumentInput, QueryInput
from app.services.milvus_service import MilvusService
from app.services.gemini_service import GeminiService
from fastapi.responses import StreamingResponse
import json

from app.tools.knowledge_functions import KnowledgeFunctions
from app.llm.llm import LLM

router = APIRouter(prefix="/knowledge", tags=["knowledge"])
logger = logging.getLogger(__name__)

user_sessions = {
    
}


@router.post("/add")
async def add_document(
    document: DocumentInput,
    milvus: MilvusService = Depends(),
    gemini: GeminiService = Depends()
):
    """Add a new document to the knowledge base."""
    try:
        embedding = await gemini.get_embedding(
            f"Question: {document.question}\nAnswer: {document.answer}"
        )
        milvus.insert_document(
            combined_question_answer=f"Question: {document.question}\nAnswer: {document.answer}",
            embedding=embedding
        )
        return {"message": "Document added successfully"}
    except Exception as e:
        logger.error(f"Failed to add document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query_knowledge(
    query: QueryInput,
    milvus: MilvusService = Depends(),
    gemini: GeminiService = Depends()
):
    """Query the knowledge base and get a response."""
    try:
        query_embedding = await gemini.get_embedding(query.question)
        similar_docs = milvus.search_similar(query_embedding)
        context = [
            {
                "question": hit['entity']['question'],
                "answer": hit['entity']['answer']
            }
            for hit in similar_docs
        ]
        response = await gemini.generate_response(query.question, context)
        return {
            "response": response
        }
    except Exception as e:
        logger.error(f"Failed to query knowledge base: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query/stream", response_model=None)
async def stream_query_response(
    query: QueryInput,
    llm: LLM = Depends(),
    knowledge_functions: KnowledgeFunctions = Depends(),
    session_id: str = Header('x-session-id')
) -> StreamingResponse:
    """Stream the response from querying the knowledge base."""
    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            existing_session = user_sessions.get(session_id, [])
            logger.info(f"Existing session Length: {len(existing_session)}")
            existing_session.append(types.Content(parts=[types.Part(text=query.question)], role='user'))

            def stream_model_response():
                return llm.get_client().stream(
                    messages=existing_session,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        tools=[
                            types.Tool(
                                function_declarations=[knowledge_functions.query_knowledge_base_tool_spec]
                            )
                        ]
                    )
                )
            async def iterate_response(response) -> AsyncGenerator[str, None]:
                for chunk in response:
                    if chunk.candidates:
                        for candidate in chunk.candidates:
                            if candidate.content:
                                for part in candidate.content.parts:
                                    if part.function_call is not None:
                                        tool_response = await knowledge_functions.call_tool(part.function_call)
                                        existing_session.append(types.Content(parts=[types.Part(text=tool_response)], role='assistant'))
                                        new_response = stream_model_response()
                                        async for chunk in iterate_response(new_response):
                                            yield chunk
                                        return 
                                    elif part.text:
                                        yield f"data: {part.text}\n\n"
            
            response = stream_model_response()
            async for chunk in iterate_response(response):
                yield chunk
            user_sessions[session_id] = existing_session

        except Exception as e:
            logger.error(f"Failed to stream query response: {e}")
            yield f"data: Error: {str(e)}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")