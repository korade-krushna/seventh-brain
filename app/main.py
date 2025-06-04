from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes.health import router as health_router
from app.routes.knowledge import router as knowledge_router
import logging
import sys
from app.dependecies import Dependencies

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(name)s:%(levelname)s:%(lineno)d - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

dependencies = Dependencies()

def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Starting up...")
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="Second Brain API",
    description="API for managing and querying a personal knowledge base using Milvus and Gemini",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(knowledge_router, dependencies=[Depends(dependencies.get_milvus), Depends(dependencies.get_gemini), Depends(dependencies.get_knowledge_functions)])

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Second Brain API",
        "docs_url": "/docs",
        "health_check": "/health",
        "knowledge_base": {
            "add_document": "/knowledge/add",
            "query": "/knowledge/query",
            "stream_query": "/knowledge/query/stream"
        }
    } 