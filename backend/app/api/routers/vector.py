# AiInternTask/chatbot_theme_identifier/backend/app/api/routers/vector.py
"""
This module defines the FastAPI router for handling vector-based document search and management.
It includes endpoints for searching documents and adding new documents to the vector database.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from ...services.vector_service import VectorService
from ...models.schemas import SearchQuery

router = APIRouter(prefix="/vector", tags=["vector"])
vector_service = VectorService()


@router.post("/search")
async def search_documents(query: SearchQuery) -> Dict[str, Any]:
    """
    search_documents endpoint to handle vector-based document search.

    Parameters
    ----------
    query : SearchQuery
        The search query containing the text to search and the number of results to return.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the search results and the total number of results.
        If an error occurs, it raises an HTTPException with a 500 status code.
    """
    try:
        results = await vector_service.search(
            query.query,
            n_results=query.n_results
        )
        return {
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-documents")
async def add_documents(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    add_documents endpoint to add new documents to the vector database.

    Parameters
    ----------
    documents : List[Dict[str, Any]]
        A list of documents to be added, where each document is represented as a dictionary.

    Returns
    -------
    Dict[str, Any]
        A dictionary indicating the status of the operation and a message.
        If an error occurs, it raises an HTTPException with a 500 status code.
    """
    try:
        await vector_service.add_documents(documents)
        return {"status": "success", "message": "Documents added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/delete-doc/{request}")
async def delete_document(request: str) -> Dict[str, Any]:
    """
    delete_document endpoint to remove a document and its associated paragraphs from the vector database.

    Parameters
    ----------
    request : str
        The unique identifier of the document to be deleted.

    Returns
    -------
    Dict[str, Any]
        A dictionary indicating the status of the deletion operation.
        If an error occurs, it raises an HTTPException with a 500 status code.
    """
    try:
        success = await vector_service.delete_document(request)
        if success:
            return {"status": "success", "message": f"Document {request} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Document {request} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleteing document: {str(e)}")
