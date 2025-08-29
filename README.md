# Document Research & Theme Identification Chatbot
----

This project is an GEMINI AI-powered chatbot that can process multiple documents, answer questions about their content, and identify common themes across documents.

[***Visit the the deployed Streamlit App***](https://pranayj97-gemini-chatbot-apiapp.hf.space)

## Features
----

- Upload and process 75+ documents (PDF, text files, and images)
- Extract text from documents using OCR for scanned files
- Ask questions in natural language about document content
- Get answers with accurate citations (document, page, paragraph)
- Identify common themes across all documents
- Clean and intuitive web interface
- Document management system
- Chat history with expandable responses

## Technology Stack
----

- Frontend: Streamlit
- Backend: FastAPI
- AI Model: Google Gemini
- Vector Database: ChromaDB
- OCR: Tesseract
- Embeddings: Sentence Transformers

## Prerequisites
----

- Python 3.8+
- Tesseract OCR
- Google AI Studio API key

## DEATAILED PROJECT DOCUMENTATION
----

[For detailed project documentation](./docs/PROJECT_DOCUMENTATION.md)

## Limitations
----
- Maximum document upload size: 100MB
- Supported file types: PDF, TXT, PNG, JPG, JPEG
- Maximum number of documents: 100
- OCR accuracy may vary based on image quality
- Response time may vary based on document size and number of documents
- Does not support persistent chat history across sessions

## Contributing
----

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
----

This project is licensed under the MIT License - see the LICENSE file for details.
