# AiInternTask/chatbot_theme_identifier/backend/app/api/routers/document.py
"""
This module defines the FastAPI router for handling document uploads and processing.
It includes endpoints for uploading documents, processing them, and adding them to a vector database.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any
from ...services.document_service import DocumentService
from ...services.vector_service import VectorService
# from ...config import Config
from icecream import ic
# import requests
# import logging

# API Configuration
API_URL = "http://localhost:8000/api/v1"


# Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])
doc_service = DocumentService()
vector_service = VectorService()


@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...), files_existing: int = 0) -> Dict[str, Any]:
    """
    upload_documents endpoint to handle the upload and processing of documents.

    Parameters
    ----------
    files : List[UploadFile], optional
        A list of uploaded files to be processed and searched for answers & themes, by default File(...)
    files_existing : int, optional
        Number of pre-existing files in streamlit session, by default 0

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the results of the document processing.
    """
    try:
        results = []
        # for file in files:
        # extension = file.filename.split('.')[-1].lower()
        # if extension not in Config.ALLOWED_EXTENSIONS:
        #     results.append({
        #         "filename": file.filename,
        #         "status": "error",
        #         "message": f"Unsupported file type: {extension}"
        #     })
        #     continue

        # content = await file.read()
        result = await doc_service.process_documents(files, files_existing)
        results.extend(result)

        ic(type(results), len(results))
        # response = requests.post(f"{API_URL}/vector/add-documents", params={"documents": results})
        await vector_service.add_documents(results)
        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
