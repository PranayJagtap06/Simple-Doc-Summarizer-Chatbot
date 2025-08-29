# AiInternTask/chatbot_theme_identifier/backend/app/services/vector_service.py
"""
This module defines the VectorService class for managing vector-based document storage and retrieval.
It uses the ChromaDB client to add documents and perform searches based on vector embeddings.
The class provides methods to add documents to a vector database and search for relevant documents based on a query.
It handles the creation of a collection if it does not already exist and provides methods for adding documents and searching for them.
The class also includes error handling and logging for debugging purposes.
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from ..config import Config
# import logging
from app import logger

# Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


class VectorService:
    """
    VectorService class for managing vector-based document storage and retrieval.
    It uses the ChromaDB client to add documents and perform searches based on vector embeddings.
    """

    def __init__(self, collection_name: str = "documents") -> None:
        """
        __init__ method to initialize the VectorService.
        It connects to the ChromaDB client and retrieves or creates a collection for storing documents.
        If the collection does not exist, it creates a new one with the specified name.

        Parameters
        ----------
        collection_name : str, optional
            The name of the collection to use for storing documents, by default "documents"
        """
        CHROMA_SETTINGS = Settings(
            anonymized_telemetry=False,
            allow_reset=False,
            is_persistent=False,
            chroma_query_request_timeout_seconds=300
        )
        self.client = chromadb.Client()
        try:
            self.collection = self.client.get_collection(collection_name)
            logger.info(f"Retrieved existing collection: {collection_name}")
        except Exception:
            logger.info(f"Creating new collection: {collection_name}")
            self.collection = self.client.create_collection(collection_name)

    async def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        add_documents method to add a list of documents to the vector database.

        Parameters
        ----------
        documents : List[Dict[str, Any]]
            A list of documents to be added, where each document is represented as a dictionary.
            Each document should contain paragraphs with their respective metadata.
        """
        try:
            for doc in documents:
                for para in doc["paragraphs"]:
                    self.collection.add(
                        documents=[para["text"]],
                        metadatas=[{
                            "doc_id": doc["id"],
                            "filename": doc["filename"],
                            "type": doc["type"],
                            "size": doc["size"],
                            "upload_time": doc["upload_time"],
                            "page": para["page"],
                            "paragraph": para["paragraph"],
                            "para_id": para["id"],
                            "text": para["text"]
                        }],
                        ids=[f"{doc['id']}_{para['id']}"]
                    )
            logger.info('Successfully added data to database')
        except Exception as e:
            logger.error(f"Error adding documents to vector DB: {e}")
            raise

    async def delete_document(self, request: str) -> bool:
        """
        Delete all paragraphs associated with a specific document ID from the vector database.

        Parameters
        ----------
        request : str
            The unique identifier of the document to delete

        Returns
        -------
        bool
            True if deletion was successful, False otherwise
        """
        try:
            # Get all IDs in the collection
            all_ids = self.collection.get()["ids"]

            # Filter IDs that start with the given request
            to_delete = [id for id in all_ids if id.startswith(f"{request}_")]

            if not to_delete:
                logger.warning(
                    f"No paragraphs found for document ID: {request}")
                return False

            # Delete all matching paragraphs
            self.collection.delete(ids=to_delete)

            logger.info(
                f"Successfully deleted document {request} ({len(to_delete)} paragraphs)")
            return True

        except Exception as e:
            logger.error(
                f"Error deleting document {request} from vector DB: {e}")
            raise

    async def search(self, query: str, n_results: int = 20) -> List[Dict[str, Any]]:
        """
        search method to search for documents in the vector database based on a query.
        It retrieves the top `n_results` documents that are most relevant to the query.

        Parameters
        ----------
        query : str
            The search query text to find relevant documents.
        n_results : int, optional
            The number of results to return, by default 20.

        Returns
        -------
        List[Dict[str, Any]]
            A list of dictionaries containing the search results, where each dictionary includes:
            - "text": The text of the document.
            - "metadata": Metadata associated with the document.
            - "distance": The distance score indicating relevance to the query.
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            searches = [{
                "text": results["documents"][0][i],  # type: ignore
                "metadata": results["metadatas"][0][i],  # type: ignore
                "distance": results["distances"][0][i] if "distances" in results else 0  # type: ignore
            } for i in range(len(results["documents"][0]))]  # type: ignore
            logger.info('Vector DB search successfully completed')
            return searches

        except Exception as e:
            logger.error(f"Error searching vector DB: {e}")
            raise
