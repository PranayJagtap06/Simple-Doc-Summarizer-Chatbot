# AiInternTask/chatbot_theme_identifier/backend/app/api/routers/chat.py
"""
This module defines the FastAPI router for handling chat queries and responses.
It includes endpoints for processing chat queries and checking the health of the chat service.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ...services.chat_service import ChatService
from ...services.vector_service import VectorService
from ...models.schemas import ChatQuery

router = APIRouter(prefix="/chat", tags=["chat"])
chat_service = ChatService(google_ai_model="gemini-2.5-flash-preview-05-20")
vector_vervice = VectorService()


@router.post("/query")
async def process_query(query: ChatQuery) -> Dict[str, Any]:
    """
    process_query endpoint to handle chat queries.

    Parameters
    ----------
    query : ChatQuery
        The chat query containing the user's question.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the answers, themes, synthesis, total documents searched, and the original query.
        If no relevant documents are found, it returns a message indicating that.
    """
    try:
        # chat_service = ChatService(google_ai_model="gemini-1.5-flash")
        # Search relevant documents
        search_results = await vector_vervice.search(query.query)

        if not search_results:
            return {
                "answers": [],
                "themes": {"themes": [], "synthesis": "No relevant documents found."},
                "total_docs_searched": 0,
                "query": query.query
            }

        # Process query and generate response
        response = await chat_service.process_query(query.query, search_results)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    health_check endpoint to check the health of the chat service.

    Returns
    -------
    Dict[str, Any]
        A dictionary indicating the health status of the chat service and the model being used.
    """
    return {"status": "healthy", "model": chat_service.model}
