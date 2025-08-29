# Document Research & Theme Identification Chatbot Documentation
----

## Table of Contents
----

- [Document Research \& Theme Identification Chatbot Documentation](#document-research--theme-identification-chatbot-documentation)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [System Architecture](#system-architecture)
  - [Prerequisites](#prerequisites)
  - [Installation Guide](#installation-guide)
    - [1. System Dependencies](#1-system-dependencies)
    - [2. Python Environment Setup](#2-python-environment-setup)
    - [3. Environment Configuration](#3-environment-configuration)
  - [Project Structure](#project-structure)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
    - [Method 1: Direct Execution](#method-1-direct-execution)
    - [Method 2: Docker Deployment](#method-2-docker-deployment)
      - [A. Single Docker Container](#a-single-docker-container)
      - [B. Using Docker Compose](#b-using-docker-compose)
  - [Usage Guide](#usage-guide)
    - [1. Document Upload](#1-document-upload)
    - [2. Querying Documents](#2-querying-documents)
    - [3. Document Management](#3-document-management)
  - [API Documentation](#api-documentation)
    - [Key Endpoints](#key-endpoints)
  - [Testing](#testing)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
  - [Performance Optimization](#performance-optimization)
  - [Security Considerations](#security-considerations)
  - [Support](#support)

## Overview
----
The Document Research & Theme Identification Chatbot is an AI-powered application that processes multiple documents, extracts information, and identifies themes across documents. It uses advanced NLP techniques to understand document content and provide intelligent responses to user queries. Basically, utilizes ***Google Gemini LLM*** under the hood.

## Features
----
- **Document Processing**
  - Support for multiple file formats (PDF, TXT, PNG, JPG, JPEG)
  - OCR capabilities for scanned documents and images
  - Text extraction and preprocessing
  - Automatic paragraph segmentation

- **Search & Analysis**
  - Vector-based document search
  - Natural language query processing
  - Theme identification across documents
  - Citation tracking (document, page, paragraph)

- **User Interface**
  - Streamlit-based web interface
  - Document library management
  - Chat history tracking
  - Real-time response generation

## System Architecture
----
- **Frontend**: Streamlit web application
- **Backend**: FastAPI REST API
- **AI Model**: Google Gemini Pro
- **Vector Database**: ChromaDB
- **OCR Engine**: Tesseract
- **Text Processing**: Sentence Transformers

## Prerequisites
----
1. Python 3.8 or higher
2. Tesseract OCR
3. Google AI Studio API key
4. Docker (optional)
5. 2GB+ RAM
6. 5GB+ disk space

## Installation Guide
----

### 1. System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y tesseract-ocr libmagic1 wget neovim docker

# Arch
sudo pacman -Syyu
sudo pacman -S tesseract tesseract-data-eng tesseract-data-osd wget neovim docker

# MacOS
brew install tesseract docker
```

### 2. Python Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

# Install Python dependencies
pip install -r chatbot-theme-identifier/requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the backend directory:
```env
GEMINI_API_KEY=your_api_key_her
```

Or `export GEMINI_API_KEY=your_api_key_here` --for Linux/MacOS


## Project Structure
----
```
chatbot_theme_identifier/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI App/endpoints
│   │   ├── core/         # Core utilities
│   │   ├── models/       # Schemas
│   │   ├── services/     # App services 
│   │   ├── main.py       # Streamlit App
│   │   └── config.py     # Configuration
│   ├── data/             # Data storage
│   ├── requirements.txt
│   └── Dockerfile
├── tests/                # Test suite
├── docs/                 # Documentation
├── demo/                 # Demo scripts
└── README.md
```

## Configuration
----
Key configuration options in `backend/app/config.py`:
```python
ALLOWED_EXTENSIONS = {"pdf", "txt", "png", "jpg", "jpeg"}
MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 200MB
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
```

## Running the Application
----

### Method 1: Direct Execution
1. Start the backend server:
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --timeout-keep-alive 300 --reload
```

2. Start the Streamlit frontend (in a new terminal):
```bash
streamlit run main.py --server.port 8501 --server.address 0.0.0.0 --server.enableCORS true --server.enableXsrfProtection true 
```

### Method 2: Docker Deployment
#### A. Single Docker Container
```bash
cd backend

# Build the Docker image
docker build -t chatbot-theme-identifier .

# Run the container
docker run -p 8501:8501 \
  --env-file ./.env \
  chatbot-theme-identifier
```

#### B. Using Docker Compose
```bash
cd backend

# Build the service and 
docker compose up -w --menu --build
```

## Usage Guide
----

### 1. Document Upload
1. Use the sidebar to upload documents
2. Supported formats: PDF, TXT, PNG, JPG, JPEG
3. Click "Process Documents" to initiate processing

### 2. Querying Documents
1. Enter your question in the main chat interface
2. Click "Search" to process the query
3. View document-specific answers and identified themes
4. Browse chat history with expandable responses

### 3. Document Management
1. Use the Document Library tab to view all uploads
2. Filter documents by type
3. Sort by upload time, filename, or size
4. Preview document content

## API Documentation
----

### Key Endpoints

1. Document Upload
```bash
POST /api/v1/documents/upload
Content-Type: multipart/form-data
```

2. Chat Query
```bash
POST /api/v1/chat/query
Content-Type: application/json
{
    "query": "your question here"
}
```

3. Vector Search
```bash
POST /api/v1/vector/search
Content-Type: application/json
{
    "query": "search text",
    "n_results": 20
}
```

## Testing
----
Run the test suite:
```bash
cd tests
pytest -v
```

## Troubleshooting
----

### Common Issues

1. **OCR Not Working**
   - Verify Tesseract installation
   - Check file permissions
   - Ensure supported image format

2. **API Connection Errors**
   - Verify API key in .env file
   - Check network connectivity
   - Confirm correct ports are exposed

3. **Memory Issues**
   - Reduce batch size
   - Limit concurrent uploads
   - Clear vector store cache

<!-- ### Logs
- Backend logs: `backend/logs/app.log`
- Streamlit logs: `~/.streamlit/logs/` -->

## Performance Optimization
1. Use batch processing for multiple documents
2. Enable caching for frequent queries
3. Optimize chunk size based on document length
4. Adjust vector search parameters

## Security Considerations
1. API key protection
2. Rate limiting
3. Input validation
4. Secure file handling
5. CORS configuration

## Support
For issues and questions:
1. Check the troubleshooting guide
2. Review existing GitHub issues
3. Create a new issue with detailed information

---
**Note**: Keep your API keys secure and never commit them to version control.

