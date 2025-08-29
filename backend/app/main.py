# AiInternTask/chatbot_theme_identifier/backend/app/main.py
"""
Main entry point for the FastAPI application.
This module initializes the FastAPI application, configures CORS, includes routers for document processing,
vector search, and chat functionalities, and defines startup and health check events.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import document, vector, chat
from .config import Config


app = FastAPI(
    title="Document Research & Theme Identification API",
    description="API for processing documents and generating themed responses",
    version="1.0.0",
    timerout=300
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

# Include routers
app.include_router(document.router, prefix="/api/v1")
app.include_router(vector.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Initialize necessary components on startup"""
    Config.init_folders()


@app.get("/api/v1/documents/upload")
async def upload_documents():
    """Endpoint for uploading documents"""
    return {"message": "Upload documents here"}


@app.get("/api/v1/vector/search")
async def vector_search():
    """Endpoint for vector search"""
    return {"message": "Perform vector search here"}


@app.get("/api/v1/chat/query")
async def chat_query():
    """Endpoint for chat queries"""
    return {"message": "Query the chat here"}


@app.get("/api/v1/vector/delete_document")
async def delete_document():
    """Endpoint for deleting a document from the vector store"""
    return {"message": "Delete a document from the vector store here"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "config": {
            "upload_folder": str(Config.UPLOAD_FOLDER),
            "vector_store": str(Config.CHROMA_PERSIST_DIR)
            }}


@app.get("/")
async def home():
    """Root endpoint"""
    return {"message": f"Welcome to the {Config.PROJECT_NAME}",
            "version": Config.API_V1_STR,
            "status": "running"}
