# AiInternTask/chatbot_theme_identifier/backend/app/services/document_service.py
"""
This module defines the DocumentService class for processing and managing document uploads.
It includes methods for processing documents, extracting text, and splitting text into paragraphs.
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from fastapi import UploadFile, HTTPException
from ..core.utils import generate_doc_id, extract_text_from_pdf, extract_text_from_image
from ..models.schemas import DocumentMetadata
from ..config import Config
from icecream import ic
# import logging
from app import logger

# Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


class DocumentService:
    """
    DocumentService class for processing and managing document uploads.
    It includes methods for processing documents, extracting text, and splitting text into paragraphs.
    It supports various file formats such as PDF, TXT, PNG, JPG, and JPEG.
    The class handles file reading, text extraction, and metadata creation for each document.
    It also provides functionality to split text into paragraphs with metadata.
    """
    def __init__(self):
        """
        __init__ method to initialize the DocumentService.
        It sets up the supported file formats based on the configuration.
        """
        self.supported_formats = Config.ALLOWED_EXTENSIONS

    async def process_documents(self, files: List[UploadFile], existing_files: int = 0) -> List[Dict[str, Any]]:
        """
        process_documents method to handle the processing of uploaded documents.
        This method reads the content of each file, extracts text based on the file type,
        generates a unique document ID, and creates metadata for each document.
        It supports PDF, TXT, PNG, JPG, and JPEG file formats.
        It returns a list of dictionaries containing the results of the processing,
        including the document ID, filename, paragraphs, and status messages.

        Parameters
        ----------
        files : List[UploadFile]
            A list of uploaded files to be processed. Each file should be an instance of UploadFile.
        existing_files : int, optional
            Number of pre-existing files in the session, by default 0

        Returns
        -------
        List[Dict[str, Any]]
            A list of dictionaries containing processed documents content.
            Each dictionary includes the document ID, filename, paragraphs, and status messages.
        """
        results = []

        for i, file in enumerate(files, 1):
            try:
                if not file.filename:
                    raise HTTPException(
                        status_code=400, 
                        detail="Filename is missing"
                    )
                
                file_extension = Path(file.filename).suffix.lower()[1:]
                if file_extension not in self.supported_formats:
                    raise HTTPException(
                        status_code=400, detail=f"Unsupported file format: {file_extension}")

                # Generate unique document ID
                doc_id = generate_doc_id(i, existing_files)
                ic(doc_id)

                # Read and process file
                text = ''
                content = await file.read()
                if file_extension == "pdf":
                    text = extract_text_from_pdf(content)
                elif file_extension in ["txt"]:
                    text = content.decode("utf-8")
                elif file_extension in ["png", "jpg", "jpeg"]:
                    text = extract_text_from_image(content)

                # Save file
                file_path = Path(Config.UPLOAD_FOLDER) / \
                    f"{doc_id}.{file_extension}"
                with open(file_path, "wb") as f:
                    f.write(content)

                # Create document metadata
                doc = DocumentMetadata(
                    id=doc_id,
                    filename=file.filename,
                    type=file_extension,
                    size=len(content),
                    upload_time=datetime.now(),
                    text=text,
                    paragraphs=self._split_into_paragraphs(text)
                )

                logger.info(f'Document {file.filename} processed successfully')

                results.append({
                    "id": doc.id,
                    "filename": doc.filename,
                    "type": doc.type,
                    "size": doc.size,
                    "upload_time": doc.upload_time.isoformat(),
                    "text": doc.text,
                    "paragraphs": doc.paragraphs,
                    "status": "success",
                    "message": "Document processed successfully"
                })

            except Exception as e:
                logger.error(f"Error processing document {file.filename}: {e}")
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "message": str(e)
                })

        return results

    def _split_into_paragraphs(self, text: str) -> List[Dict[str, Any]]:
        """
        _split_into_paragraphs method to split the extracted text into paragraphs.
        This method processes the text, splits it into paragraphs based on page sections,
        and returns a list of dictionaries containing metadata for each paragraph.

        Parameters
        ----------
        text : str
            The extracted text from the document. It is expected to be a string containing
            text from one or more pages, with each page section starting with "[Page X]".
            It splits the text into paragraphs, ensuring that each paragraph has a minimum length
            of 50 characters to be considered substantial. Each paragraph is assigned a unique ID
            based on its page number and paragraph index, along with its page number and text content.

        Returns
        -------
        List[Dict[str, Any]]
            A list of dictionaries, where each dictionary contains metadata for a paragraph.
            Each dictionary includes:
            - "id": Unique identifier for the paragraph (e.g., "p1_1" for page 1, paragraph 1).
            - "page": The page number where the paragraph is located.
            - "paragraph": The index of the paragraph on that page.
            - "text": The text content of the paragraph.
        """
        paragraphs = []
        current_page = 1

        for page_section in text.split("[Page "):
            if not page_section.strip():
                continue

            try:
                # Extract page number if present
                if page_section[0].isdigit():
                    page_num, content = page_section.split("]", 1)
                    current_page = int(page_num)
                else:
                    content = page_section

                # Split into paragraphs
                for para_idx, para in enumerate(content.split("\n\n")):
                    if len(para.strip()) >= 100:  # Only substantial paragraphs
                        paragraphs.append({
                            "id": f"p{current_page}_{para_idx + 1}",
                            "page": current_page,
                            "paragraph": para_idx + 1,
                            "text": para.strip()
                        })

            except Exception as e:
                logger.error(f"Error processing page section: {e}")
                continue

        return paragraphs
