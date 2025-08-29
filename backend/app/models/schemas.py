# AiInternTask/chatbot_theme_identifier/backend/app/models/schemas.py
"""
AiInternTask/chatbot_theme_identifier/backend/app/models/schemas.py
This module defines the Pydantic models for the API schemas used in the application.
It includes models for document metadata, search queries, chat queries, and responses.
health_check endpoint to check the health of the chat service.
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class DocumentMetadata(BaseModel):
    """
    DocumentMetadata class to represent the metadata of a document.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
    id : str
        Unique identifier for the document.
    filename : str
        Name of the document file.
    type : str
        Type of the document (e.g., PDF, TXT, etc.).
    size : int
        Size of the document in bytes.
    upload_time : datetime
        Time when the document was uploaded.
    text : str
        Extracted text content from the document.
    paragraphs : List[Dict[str, Any]]
        List of paragraphs extracted from the document, each represented as a dictionary.
    """
    id: str
    filename: str
    type: str
    size: int
    upload_time: datetime
    text: str
    paragraphs: List[Dict[str, Any]]


class SearchQuery(BaseModel):
    """
    SearchQuery class to represent the search query parameters.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
    query : str
        The text to search for in the documents.
    n_results : int, optional
        The number of results to return, by default 20.
    """
    query: str
    n_results: int = 20


class SearchResponse(BaseModel):
    """
    SearchResponse class to represent the response of a search query.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
    documents : List[Dict[str, Any]]
        List of documents that match the search query, each represented as a dictionary.
    total_results : int
        Total number of results found for the search query.
    """
    documents: List[Dict[str, Any]]
    total_results: int


class ChatQuery(BaseModel):
    """
    ChatQuery class to represent the chat query parameters.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
    query : str
        The user's question or query to be processed by the chat service.
    """
    query: str


class ThemeAnalysis(BaseModel):
    """
    ThemeAnalysis class to represent the analysis of themes in the chat response.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
    themes : List[Dict[str, Any]]
        List of themes identified in the chat response, each represented as a dictionary.
    synthesis : Optional[str]
        A synthesis of the themes, providing a summary or conclusion based on the identified themes.
    """
    themes: List[Dict[str, Any]]
    synthesis: Optional[str]


class ChatResponse(BaseModel):
    """
    ChatResponse class to represent the response of a chat query.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
    query : str
        The original query made by the user.
    timestamp : datetime
        The timestamp when the response was generated.
    answers : List[Dict[str, Any]]
        List of answers generated in response to the query, each represented as a dictionary.
    themes : ThemeAnalysis
        Analysis of themes identified in the chat response.
    total_docs_searched: int
        The total number of documents that were searched to generate the response.
    """
    query: str
    timestamp: datetime
    answers: List[Dict[str, Any]]
    themes: ThemeAnalysis
    total_docs_searched: int


class DocumentResponse(BaseModel):
    """
    DocumentResponse class to represent the response after processing a document upload.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
    id : str
        Unique identifier for the uploaded document.
    filename: str
        The name of the uploaded document file.
    status: str
        The status of the document processing, indicating whether it was successful or encountered an error.
    message: str
        The status of the document processing, indicating success or failure, and a message providing additional information.
    """
    id: str
    filename: str
    status: str
    message: str
