# AiInternTask/chatbot_theme_identifier/backend/app/core/utils.py
"""
This module provides utility functions for document processing,
including generating unique document IDs, extracting text from PDFs and images,
and cleaning and splitting text into paragraphs with metadata.
"""
# import uuid
import fitz
import io
import numpy as np
from PIL import Image
import pytesseract
# import logging
from app import logger
from typing import List, Dict, Any

# logger = logging.getLogger(__name__)


def generate_doc_id(numb: int = 0, numb_files_exists: int = 0) -> str:
    """
    generate_doc_id generates a unique document ID based on the number of existing files.
    This function creates a document ID in the format "DOCXXX", where XXX is a zero-padded number
    that increments based on the number of files already processed.
    It ensures that the document ID is unique and sequentially numbered based on the existing files.

    Parameters
    ----------
    numb : int, optional
        The number to be added to the document ID, by default 0
    numb_files_exists : int, optional
        The number of files that already exist in the system, by default 0

    Returns
    -------
    Optional[str]
        Returns a string representing the document ID in the format "DOCXXX", where XXX is a zero-padded number.
    """
    try:
        id_list: List[int] = np.load('doc_id_list.npy', allow_pickle=True).tolist()
    except Exception as e:
        logger.error(f"File not found: {e}. Initializing empty document ID list.")
        id_list: List[int] = []
        np.save('doc_id_list.npy', id_list)

    ini_doc_num: int = sorted(list(set(id_list)))[-1] if len(id_list) else 1
    doc_num: int = numb_files_exists + numb
    doc_id: str = f"DOC{doc_num:03d}"
    if doc_num >= ini_doc_num and doc_num not in id_list:
        id_list.append(doc_num)
        np.save('doc_id_list.npy', id_list)
        return doc_id
    else:
        doc_num = ini_doc_num + 1
        id_list.append(doc_num)
        np.save('doc_id_list.npy', id_list)
        return f"DOC{doc_num:03d}"

    # return f"DOC{str(uuid.uuid4())[:8].upper()}"
    return 


def extract_text_from_pdf(content: bytes) -> str:
    """
    extract_text_from_pdf extracts text from a PDF document.
    This function uses the PyMuPDF library to open a PDF document from bytes,
    iterates through each page, and extracts text. It also handles images within the PDF,
    extracting text from images using Tesseract OCR. The extracted text is returned as a single string,
    with each page's text prefixed by its page number. If any errors occur during processing,
    they are logged, and an empty string is returned.

    Parameters
    ----------
    content : bytes
        The content of the PDF document as bytes.
        This content is expected to be in PDF format.

    Returns
    -------
    str
        Returns a string containing the extracted text from the PDF document.
        Each page's text is prefixed with its page number, and text from images is also included.
        If an error occurs during extraction, an empty string is returned.
    """
    try:
        with fitz.open(stream=content, filetype="pdf") as pdf_doc:
            text = ""
            for page_num, page in enumerate(pdf_doc, 1): # type: ignore
                text += f"[Page {page_num}]\n{page.get_text()}\n\n"

                # Extract text from images in PDF
                for image in page.get_images():
                    try:
                        xref = image[0]
                        base_image = pdf_doc.extract_image(xref)
                        image_text = extract_text_from_image(
                            base_image["image"])
                        if image_text.strip():
                            text += f"[Image Text Page {page_num}]\n{image_text}\n\n"
                    except Exception as e:
                        logger.error(f"Error processing PDF image: {e}")

            return text.strip()
    except Exception as e:
        logger.error(f"Error extracting PDF text: {e}")
        return ""


def extract_text_from_image(content: bytes) -> str:
    """
    extract_text_from_image extracts text from an image using Tesseract OCR.
    This function takes the content of an image as bytes, opens it using PIL,
    and uses pytesseract to extract text from the image. If any errors occur during
    the extraction process, they are logged, and an empty string is returned.

    Parameters
    ----------
    content : bytes
        The content of the image as bytes.
        This content is expected to be in a format that PIL can open (e.g., PNG, JPEG).

    Returns
    -------
    str
        Returns a string containing the extracted text from the image.
    """
    try:
        image = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(image)
    except Exception as e:
        logger.error(f"Error extracting image text: {e}")
        return ""


def clean_and_split_text(text: str) -> List[Dict[str, Any]]:
    """
    clean_and_split_text  method to split the extracted text into paragraphs.
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
                if len(para.strip()) >= 50:  # Only substantial paragraphs
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
